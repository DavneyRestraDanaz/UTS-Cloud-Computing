from flask import Flask, render_template_string, request, redirect, url_for
import pymysql
import sys
from datetime import datetime

app = Flask(__name__)

# Fungsi untuk koneksi ke database
def get_db_connection():
    try:
        connection = pymysql.connect(
            host='ecommerce-db1.cxwca0y02oyq.ap-southeast-1.rds.amazonaws.com',
            user='admin',
            password='Ikomersdb1!',
            database='ecommerce'
        )
        return connection
    except Exception as e:
        print(f"Error koneksi database: {e}")
        return None

# Route untuk halaman utama
@app.route('/')
def home():
    try:
        # Dapatkan koneksi database
        db = get_db_connection()
        if not db:
            return "<h1>Error koneksi database</h1>"
            
        cursor = db.cursor()
        # Ambil data produk
        cursor.execute("SELECT nama_produk, harga, url_gambar FROM produk")
        products = cursor.fetchall()
        cursor.close()
        db.close()
        
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
                
                .nav-buttons {
                    margin: 20px 0;
                    text-align: right;
                }
                
                .add-btn {
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                    text-decoration: none;
                    display: inline-block;
                }
                
                .add-btn:hover {
                    background-color: #27ae60;
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
            
            <div class="nav-buttons">
                <a href="/add" class="add-btn">+ Tambah Produk Baru</a>
            </div>
            
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

# Route untuk halaman form tambah produk
@app.route('/add')
def add_product_form():
    html = '''
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tambah Produk Baru</title>
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
            
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .form-group {
                margin-bottom: 15px;
            }
            
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            
            input, textarea {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            
            .btn-submit {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            
            .btn-submit:hover {
                background-color: #2980b9;
            }
            
            .btn-cancel {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                margin-right: 10px;
                text-decoration: none;
                display: inline-block;
            }
            
            .btn-cancel:hover {
                background-color: #c0392b;
            }
            
            .buttons {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Tambah Produk Baru</h1>
        </header>
        
        <div class="container">
            <form action="/add" method="post">
                <div class="form-group">
                    <label for="nama_produk">Nama Produk:</label>
                    <input type="text" id="nama_produk" name="nama_produk" required>
                </div>
                
                <div class="form-group">
                    <label for="harga">Harga (Rp):</label>
                    <input type="number" id="harga" name="harga" min="1000" required>
                </div>
                
                <div class="form-group">
                    <label for="url_gambar">URL Gambar:</label>
                    <input type="url" id="url_gambar" name="url_gambar" required>
                </div>
                
                <div class="buttons">
                    <a href="/" class="btn-cancel">Batal</a>
                    <button type="submit" class="btn-submit">Simpan</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# Route untuk memproses form tambah produk
@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        try:
            # Ambil data dari form
            nama_produk = request.form['nama_produk']
            harga = float(request.form['harga'])
            url_gambar = request.form['url_gambar']
            
            # Validasi data
            if not nama_produk or not url_gambar or harga <= 0:
                return "<h1>Error</h1><p>Semua field harus diisi dengan benar</p>"
            
            # Koneksi ke database
            db = get_db_connection()
            if not db:
                return "<h1>Error koneksi database</h1>"
                
            # Insert data ke database
            cursor = db.cursor()
            sql = "INSERT INTO produk (nama_produk, harga, url_gambar) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nama_produk, harga, url_gambar))
            db.commit()
            cursor.close()
            db.close()
            
            # Redirect ke halaman utama
            return redirect(url_for('home'))
            
        except Exception as e:
            return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
