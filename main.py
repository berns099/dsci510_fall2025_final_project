from load import *
from config import *

# if __name__ == "__main__":
    # # Create a data directory
    # os.makedirs(DATA_DIR, exist_ok=True)
    #
    # # --- Kaggle Data ---
    # # We'll use the classic Titanic dataset
    # kaggle_df = get_kaggle_data(dataset_slug=TITANIC_DATASET_SLUG, extract_dir=DATA_DIR)
    # if kaggle_df is not None:
    #     print(f"\nKaggle (Titanic) Data Head:\n{kaggle_df.head()}")
    #     plot_statistics(kaggle_df, 'Titanic', result_dir=RESULTS_DIR)
    # print("\n" + "=" * 50 + "\n")
    #
    # # --- Web CSV Data ---
    # # We'll use the Iris dataset from a public repo
    # web_df = get_web_csv_data(IRIS_URL)
    # if web_df is not None:
    #     print(f"\nWeb (Iris) Data Head:\n{web_df.head()}")
    #     plot_statistics(web_df, 'Iris', result_dir=RESULTS_DIR)
    # print("\n" + "=" * 50 + "\n")

    # --- Aviation scrapped data---
    # We'll scrape a table of the largest companies
    # process data firsts
#get_accident_table_data(AVIATION_ACCIDENTS)
#get_trend_data(SEARCH_QUERIES)
get_enplanement(ENPLANEMENTS_CSV)
    # plot results
    # plot_statistics(plot_df.dropna(), 'Wikipedia_Companies', result_dir=RESULTS_DIR)
    # print("\n" + "=" * 50 + "\n")

    # print("\n--- Data collection and plotting complete. Check the 'results' directory. ---")