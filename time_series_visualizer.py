import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Import the data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    index_col="date",
    parse_dates=["date"]
)


# Clean the data by removing the bottom 2.5%
# and top 2.5% of page views
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Make a copy of the data
    df_line = df.copy()

    # Create the figure
    fig, ax = plt.subplots(figsize=(12, 5))

    # Draw the line plot
    ax.plot(
        df_line.index,
        df_line["value"]
    )

    # Set title and labels
    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save and return the figure
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Make a copy of the data
    df_bar = df.copy()

    # Create year and month columns
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    # Calculate average daily page views
    df_bar = df_bar.groupby(
        ["year", "month"]
    )["value"].mean().unstack()

    # Put months in chronological order
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    df_bar = df_bar.reindex(columns=months)

    # Create the bar plot
    fig = df_bar.plot(
        kind="bar",
        figsize=(12, 7)
    ).get_figure()

    # Set labels
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    # Set legend
    plt.legend(
        title="Months",
        labels=months
    )

    # Adjust layout
    plt.tight_layout()

    # Save and return the figure
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Make a copy of the data
    df_box = df.copy()

    # Reset the index
    df_box.reset_index(inplace=True)

    # Create year and month columns
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Set the correct month order
    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    # Create two box plots
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(16, 5)
    )

    # Year-wise box plot
    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )

    axes[0].set_title(
        "Year-wise Box Plot (Trend)"
    )
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        order=month_order,
        ax=axes[1]
    )

    axes[1].set_title(
        "Month-wise Box Plot (Seasonality)"
    )
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Adjust layout
    plt.tight_layout()

    # Save and return the figure
    fig.savefig("box_plot.png")
    return fig