from flask import Flask, render_template_string
import pymysql
import sys
from datetime import datetime

app = Flask(__name__)

try:
    # Koneksi ke Database
    db = pymysql.connect(
        host='ecommerce-db1.cxwca0y02oyq.ap-southeast-1.rds.amazonaws.com',
        user='admin',
        password='Ikomersdb1!',
        database='ecommerce'
    )
except Exception as e:
    print(f"Error koneksi database: {e}")
    sys.exit(1)

@app.route('/')
def home():
    try:
        cursor = db.cursor()
        # Hapus kolom deskripsi dari query karena tidak ada di tabel
        cursor.execute("SELECT nama_produk, harga, url_gambar FROM produk")
        products = cursor.fetchall()
        
        html = '''
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>E-Commerce App</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                
                header {
                    background-color: #3498db;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 20px;
                    border-radius: 5px;
                }
                
                h1 {
                    margin: 0;
                }
                
                .product-container {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }
                
                .product-card {
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    overflow: hidden;
                    transition: transform 0.3s;
                }
                
                .product-card:hover {
                    transform: translateY(-5px);
                }
                
                .product-img {
                    width: 100%;
                    height: 180px;
                    object-fit: cover;
                }
                
                .product-info {
                    padding: 15px;
                }
                
                .product-name {
                    font-weight: bold;
                    font-size: 18px;
                    margin-bottom: 5px;
                }
                
                .product-price {
                    color: #e74c3c;
                    font-size: 18px;
                    font-weight: bold;
                    margin-top: 10px;
                }
                
                footer {
                    margin-top: 40px;
                    text-align: center;
                    color: #666;
                    font-size: 14px;
                    padding: 20px;
                    border-top: 1px solid #ddd;
                }
                
                @media (max-width: 600px) {
                    .product-container {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Daftar Produk</h1>
                <p>Aplikasi E-Commerce Cloud Computing</p>
            </header>
            
            <div class="product-container">
                {% for nama, harga, url in products %}
                <div class="product-card">
                    <img src="{{ url }}" alt="{{ nama }}" class="product-img">
                    <div class="product-info">
                        <div class="product-name">{{ nama }}</div>
                        <div class="product-price">Rp {{ "{:,.0f}".format(harga) }}</div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <footer>
                &copy; {{ current_year }} E-Commerce App | UTS Cloud Computing
            </footer>
        </body>
        </html>
        '''
        
        current_year = datetime.now().year
        return render_template_string(html, products=products, current_year=current_year)
    
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
