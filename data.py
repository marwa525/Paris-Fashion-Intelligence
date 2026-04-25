import requests
import pandas as pd
import time

def fetch_brand_data(
    api_key,
    brands=None,
    time_period='Last 30 days'
):
    if brands is None:
        brands = [
            'Louis Vuitton',
            'Hermes',
            'Chanel',
            'Dior',
            'Balenciaga'
        ]

    positive_words = [
        'growth', 'record', 'success',
        'luxury', 'iconic', 'innovative',
        'profit', 'revenue', 'winning',
        'best', 'top', 'leading',
        'award', 'launch', 'expansion'
    ]

    negative_words = [
        'decline', 'loss', 'failing',
        'controversy', 'problem', 'crisis',
        'drop', 'fall', 'worst', 'scandal',
        'boycott', 'lawsuit', 'criticism'
    ]

    results = []

    for brand in brands:
        print(f"Fetching {brand}...")

        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={brand}&"
            f"language=en&"
            f"sortBy=relevancy&"
            f"pageSize=100&"
            f"apiKey={api_key}"
        )

        response = requests.get(url)
        data = response.json()

        if data['status'] == 'ok':
            articles = data['articles']
            total = len(articles)
            positive = 0
            negative = 0

            for article in articles:
                title = str(
                    article['title']
                ).lower()

                if any(
                    w in title
                    for w in positive_words
                ):
                    positive += 1

                if any(
                    w in title
                    for w in negative_words
                ):
                    negative += 1

            neutral = total - positive - negative

            sentiment_score = round(
                (positive - negative) /
                total * 100
                if total > 0 else 0, 1
            )

            results.append({
                'brand': brand,
                'total_articles': total,
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'sentiment_score': sentiment_score
            })

            time.sleep(1)

    df = pd.DataFrame(results)
    df = df.sort_values(
        'sentiment_score',
        ascending=False
    ).reset_index(drop=True)

    return df