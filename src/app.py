import h2o
from h2o.estimators.aggregator import H2OAggregatorEstimator
from h2o_wave import Q, app, data, main, ui
from h2o_wave.core import Expando


@app("/")
async def serve(q: Q) -> None:
    """
    Handle interactions from the browser such as new arrivals and button clicks
    :param q: Query argument from the H2O Wave server
    :return: None
    """
    print("Handling a user event.")

    if not q.client.initialized:
        setup_app(q)
        show_table(q)

    if q.args.table:
        show_table(q)
    elif q.args.plot:
        show_plot(q)
    elif q.args.x_variable_dropdown is not None:

        q.client.x_variable = q.args.x_variable_dropdown
        q.client.y_variable = q.args.y_variable_dropdown

        show_plot(q)

    await q.page.save()


def setup_app(q: Q) -> None:
    """
    Activities that happen the first time someone comes to this app, such as user variables and home page cards
    :param q: Query argument from the H2O Wave server
    :return: None
    """
    print("Setting up the app for a new browser tab.")

    q.page["meta"] = ui.meta_card(
        box="",
        layouts=[
            ui.layout(
                breakpoint="xs",
                zones=[ui.zone("header"), ui.zone("navigation"), ui.zone("content")],
            )
        ],
    )
    q.page["header"] = ui.header_card(
        box="header",
        title="Data Aggregation",
        subtitle="Understand variable relationships for datasets with Millions of data points.",
    )
    q.page["tabs"] = ui.tab_card(
        box="navigation",
        value="",
        link=False,
        name="",
        items=[
            ui.tab("table", "Aggregated Table"),
            ui.tab("plot", "Aggregated Plot"),
        ],
    )

    set_aggregated_data_information(q.client)
    q.client.initialized = True


def show_table(q: Q) -> None:
    """
    Creating the UI when the user wants to view the data as a table
    :param q: Query argument from the H2O Wave server
    :return: None
    """
    print("Creating the table view.")

    del q.page["plot_view"]
    df = q.client.aggregated_data

    q.page["table_view"] = ui.form_card(
        box="content",
        items=[
            ui.table(
                name="aggregated_data_table",
                columns=[
                    ui.table_column(
                        name=str(x),
                        label=str(x),
                        sortable=True,
                        filterable=True,
                        link=False,
                    )
                    for x in df.columns.values
                ],
                rows=[
                    ui.table_row(
                        name=str(i),
                        cells=[str(df[col].values[i]) for col in df.columns.values],
                    )
                    for i in range(len(df))
                ],
                downloadable=True,
            )
        ],
    )


def show_plot(q: Q) -> None:
    """
    Creating the UI when the user want to view the data as a plot
    :param q: Query argument from the H2O Wave server
    :return: None
    """
    print("Creating the plot view.")

    del q.page["table_view"]
    df = q.client.aggregated_data

    q.page["plot_view"] = ui.form_card(
        box="content",
        items=[
            ui.text_xl(
                f"Aggregated Data {q.client.x_variable} by {q.client.y_variable}"
            ),
            ui.inline(
                [
                    ui.dropdown(
                        name="x_variable_dropdown",
                        label="X Variable",
                        value=q.client.x_variable,
                        choices=[ui.choice(col, col) for col in df.columns.values],
                        trigger=True,
                    ),
                    ui.dropdown(
                        name="y_variable_dropdown",
                        label="Y Variable",
                        value=q.client.y_variable,
                        choices=[ui.choice(col, col) for col in df.columns.values],
                        trigger=True,
                    ),
                ]
            ),
            ui.visualization(
                data=data(
                    fields=df.columns.tolist(),
                    rows=df.values.tolist(),
                    pack=True,
                ),
                plot=ui.plot(
                    marks=[
                        ui.mark(
                            type="point",
                            x=f"={q.client.x_variable}",
                            x_title=f"{q.client.x_variable}",
                            y=f"={q.client.y_variable}",
                            y_title=f"{q.client.y_variable}",
                            shape="circle",
                            size="=counts",
                        )
                    ]
                ),
            ),
        ],
    )


def set_aggregated_data_information(client_state: Expando) -> None:
    """
    Creating the aggregated dataset from a mocked 1M row dataset
    :param client_state: The state of the each browser tab visiting this app
    :return: None
    """
    print("Creating the aggregated dataset.")

    h2o.init()

    h2o_df = h2o.create_frame(
        rows=1000000,
        cols=5,
        categorical_fraction=0.6,
        integer_fraction=0,
        binary_fraction=0,
        real_range=100,
        integer_range=100,
        missing_fraction=0,
        seed=1234,
    )

    aggregator = H2OAggregatorEstimator(target_num_exemplars=100)
    aggregator.train(training_frame=h2o_df)

    aggregated_data = aggregator.aggregated_frame.as_data_frame(use_pandas=True)
    aggregated_data = aggregated_data.sort_values("counts", ascending=False)

    h2o.cluster().shutdown()

    client_state.x_variable = aggregated_data.columns[0]
    client_state.y_variable = aggregated_data.columns[1]
    client_state.aggregated_data = aggregated_data
