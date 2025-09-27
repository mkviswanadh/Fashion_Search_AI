def display_products(results_df):
    """
    Displays each product with its image on the left and a visually rich table of product details on the right.
    """
    import pandas as pd
    from IPython.display import display, HTML

    if isinstance(results_df, pd.Series):
        results_df = pd.DataFrame([results_df])

    if results_df.empty:
        print("No matching products found.")
        return

    html = """
    <style>
        .product-card {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            background-color: #ffffff;
        }
        .product-image {
            flex: 0 0 200px;
        }
        .product-image img {
            width: 180px;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        .product-details {
            margin-left: 30px;
            flex: 1;
            display: flex;
            align-items: center;
        }
        .product-table {
            width: 100%;
            max-width: 500px;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }
        .product-table td {
            padding: 10px 12px;
            border: 1px solid #e0e0e0;
            text-align: left;
        }
        .product-table td:first-child {
            font-weight: bold;
            background-color: #f8f8f8;
            color: #333;
            width: 130px;
        }
        .highlight {
            color: #d63384;
            font-weight: bold;
        }
    </style>
    """

    for _, row in results_df.iterrows():
        html += f'''
        <div class="product-card">
            <div class="product-image">
                <img src="{row['img']}" alt="Product Image">
            </div>
            <div class="product-details">
                <table class="product-table">
                    <tr>
                        <td>Name</td>
                        <td class="highlight">{row['name']}</td>
                    </tr>
                    <tr>
                        <td>Brand</td>
                        <td>{row['brand']}</td>
                    </tr>
                    <tr>
                        <td>Price</td>
                        <td><span class="highlight">₹{row['price']}</span></td>
                    </tr>
                    <tr>
                        <td>Rating</td>
                        <td>⭐ {round(row['avg_rating'], 2)} ({row.get('ratingCount', 'N/A')} ratings)</td>
                    </tr>
                </table>
            </div>
        </div>
        '''

    return html
