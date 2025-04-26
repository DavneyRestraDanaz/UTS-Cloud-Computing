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
        cursor.execute("SELECT nama_produk, harga, url_gambar FROM produk")
        products = cursor.fetchall()
        
        html = '''
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>E-Commerce App</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <style>
                :root {
                    --primary: #4361ee;
                    --secondary: #3a0ca3;
                    --accent: #f72585;
                    --light: #f8f9fa;
                    --dark: #212529;
                    --gray: #6c757d;
                    --success: #38b000;
                    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    --radius: 8px;
                }
                
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Poppins', sans-serif;
                    background-color: #f5f7fa;
                    color: var(--dark);
                    line-height: 1.6;
                }
                
                /* Navbar */
                .navbar {
                    background: linear-gradient(135deg, var(--primary), var(--secondary));
                    color: white;
                    padding: 1.2rem 0;
                    box-shadow: var(--shadow);
                    position: sticky;
                    top: 0;
                    z-index: 100;
                }
                
                .container {
                    width: 90%;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 20px;
                }
                
                .navbar-container {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .logo {
                    font-size: 1.8rem;
                    font-weight: 700;
                    color: white;
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                }
                
                .logo i {
                    margin-right: 10px;
                }
                
                /* Header Banner */
                .banner {
                    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://images.unsplash.com/photo-1607082350899-7e105aa886ae?q=80&w=2070') no-repeat center center/cover;
                    color: white;
                    text-align: center;
                    padding: 3.5rem 1rem;
                    margin-bottom: 2rem;
                }
                
                .banner-content {
                    max-width: 800px;
                    margin: 0 auto;
                }
                
                .banner h1 {
                    font-size: 2.5rem;
                    margin-bottom: 1rem;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }
                
                .banner p {
                    font-size: 1.1rem;
                    margin-bottom: 0;
                    opacity: 0.9;
                }
                
                /* Product Section */
                .section-title {
                    text-align: center;
                    margin-bottom: 2rem;
                    font-size: 1.8rem;
                    color: var(--dark);
                    position: relative;
                    padding-bottom: 10px;
                }
                
                .section-title::after {
                    content: '';
                    position: absolute;
                    bottom: 0;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 50px;
                    height: 3px;
                    background-color: var(--accent);
                    border-radius: 10px;
                }
                
                .product-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                    gap: 25px;
                    margin-bottom: 3rem;
                }
                
                .product-card {
                    background-color: white;
                    border-radius: var(--radius);
                    overflow: hidden;
                    box-shadow: var(--shadow);
                    transition: all 0.3s ease;
                    position: relative;
                }
                
                .product-card:hover {
                    transform: translateY(-10px);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
                }
                
                .card-badge {
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background-color: var(--accent);
                    color: white;
                    font-size: 0.8rem;
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-weight: 500;
                    z-index: 10;
                }
                
                .product-img-container {
                    height: 220px;
                    overflow: hidden;
                    position: relative;
                    background: #f5f5f5;
                }
                
                .product-img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transition: transform 0.5s ease;
                }
                
                .product-card:hover .product-img {
                    transform: scale(1.08);
                }
                
                .product-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.2);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                
                .product-card:hover .product-overlay {
                    opacity: 1;
                }
                
                .overlay-btn {
                    background-color: white;
                    color: var(--dark);
                    border: none;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 5px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                
                .overlay-btn:hover {
                    background-color: var(--primary);
                    color: white;
                    transform: scale(1.1);
                }
                
                .product-info {
                    padding: 20px;
                }
                
                .product-name {
                    font-weight: 600;
                    font-size: 1.1rem;
                    margin-bottom: 10px;
                    color: var(--dark);
                }
                
                .product-price {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-top: 15px;
                    border-top: 1px solid #f0f0f0;
                    padding-top: 15px;
                }
                
                .price {
                    font-size: 1.2rem;
                    font-weight: 700;
                    color: var(--primary);
                }
                
                .cart-btn {
                    background-color: var(--success);
                    color: white;
                    border: none;
                    border-radius: 50%;
                    width: 36px;
                    height: 36px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                
                .cart-btn:hover {
                    background-color: #2d9200;
                    transform: scale(1.1);
                }
                
                /* CTA Section */
                .cta-section {
                    background-color: var(--primary);
                    color: white;
                    padding: 3rem 0;
                    text-align: center;
                    margin: 3rem 0;
                }
                
                .cta-content {
                    max-width: 800px;
                    margin: 0 auto;
                }
                
                .cta-title {
                    font-size: 2rem;
                    margin-bottom: 1rem;
                }
                
                .cta-text {
                    margin-bottom: 1.5rem;
                    opacity: 0.9;
                }
                
                .cta-btn {
                    display: inline-block;
                    background-color: white;
                    color: var(--primary);
                    text-decoration: none;
                    padding: 12px 30px;
                    border-radius: 50px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    border: 2px solid white;
                }
                
                .cta-btn:hover {
                    background-color: transparent;
                    color: white;
                }
                
                /* Footer */
                .footer {
                    background-color: #212529;
                    color: white;
                    padding: 3rem 0 1.5rem;
                }
                
                .footer-container {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 30px;
                }
                
                .footer-heading {
                    font-size: 1.3rem;
                    margin-bottom: 1.5rem;
                    position: relative;
                    padding-bottom: 10px;
                }
                
                .footer-heading::after {
                    content: '';
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    width: 40px;
                    height: 2px;
                    background-color: var(--accent);
                }
                
                .footer-text {
                    opacity: 0.8;
                    margin-bottom: 1.5rem;
                    line-height: 1.6;
                }
                
                .footer-links {
                    list-style: none;
                    padding: 0;
                }
                
                .footer-links li {
                    margin-bottom: 0.8rem;
                }
                
                .footer-links a {
                    color: white;
                    opacity: 0.8;
                    text-decoration: none;
                    transition: all 0.3s ease;
                }
                
                .footer-links a:hover {
                    opacity: 1;
                    padding-left: 5px;
                    color: var(--accent);
                }
                
                .social-icons {
                    display: flex;
                    margin-top: 1.5rem;
                }
                
                .social-icon {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                    margin-right: 10px;
                    transition: all 0.3s ease;
                    text-decoration: none;
                }
                
                .social-icon:hover {
                    background-color: var(--accent);
                    transform: translateY(-3px);
                }
                
                .copyright {
                    text-align: center;
                    margin-top: 2rem;
                    padding-top: 1.5rem;
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    font-size: 0.9rem;
                    opacity: 0.7;
                }
                
                @media (max-width: 768px) {
                    .product-grid {
                        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                    }
                    
                    .banner h1 {
                        font-size: 2rem;
                    }
                }
            </style>
        </head>
        <body>
            <!-- Navbar -->
            <nav class="navbar">
                <div class="container navbar-container">
                    <a href="#" class="logo">
                        <i class="fas fa-shopping-bag"></i> TechStore
                    </a>
                    <div>
                        <i class="fas fa-bars"></i>
                    </div>
                </div>
            </nav>
            
            <!-- Banner -->
            <section class="banner">
                <div class="banner-content">
                    <h1>Produk Berkualitas dari Cloud</h1>
                    <p>Temukan berbagai produk teknologi terbaik dengan harga terjangkau</p>
                </div>
            </section>
            
            <!-- Product Section -->
            <section class="container">
                <h2 class="section-title">Katalog Produk</h2>
                <div class="product-grid">
                    {% for nama, harga, url in products %}
                    <div class="product-card">
                        {% if loop.index is divisible by 3 %}
                        <div class="card-badge">New</div>
                        {% endif %}
                        
                        <div class="product-img-container">
                            <img src="{{ url }}" alt="{{ nama }}" class="product-img">
                            <div class="product-overlay">
                                <button class="overlay-btn">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="overlay-btn">
                                    <i class="fas fa-heart"></i>
                                </button>
                            </div>
                        </div>
                        
                        <div class="product-info">
                            <h3 class="product-name">{{ nama }}</h3>
                            <div class="product-price">
                                <div class="price">Rp {{ "{:,.0f}".format(harga) }}</div>
                                <button class="cart-btn">
                                    <i class="fas fa-shopping-cart"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>
            
            <!-- CTA Section -->
            <section class="cta-section">
                <div class="container cta-content">
                    <h2 class="cta-title">Dapatkan Promo Menarik</h2>
                    <p class="cta-text">Daftar sekarang dan dapatkan diskon 10% untuk pembelian pertama Anda</p>
                    <a href="#" class="cta-btn">Daftar Sekarang</a>
                </div>
            </section>
            
            <!-- Footer -->
            <footer class="footer">
                <div class="container footer-container">
                    <div>
                        <h3 class="footer-heading">TechStore</h3>
                        <p class="footer-text">Tempat terbaik untuk menemukan produk teknologi berkualitas dengan harga terjangkau.</p>
                        <div class="social-icons">
                            <a href="#" class="social-icon"><i class="fab fa-facebook-f"></i></a>
                            <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
                            <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
                            <a href="#" class="social-icon"><i class="fab fa-linkedin-in"></i></a>
                        </div>
                    </div>
                    
                    <div>
                        <h3 class="footer-heading">Link Cepat</h3>
                        <ul class="footer-links">
                            <li><a href="#">Beranda</a></li>
                            <li><a href="#">Produk</a></li>
                            <li><a href="#">Tentang Kami</a></li>
                            <li><a href="#">Kontak</a></li>
                        </ul>
                    </div>
                    
                    <div>
                        <h3 class="footer-heading">Kontak</h3>
                        <ul class="footer-links">
                            <li><i class="fas fa-map-marker-alt"></i> Jl. Cloud Computing No.1</li>
                            <li><i class="fas fa-phone"></i> +62 812 3456 7890</li>
                            <li><i class="fas fa-envelope"></i> info@techstore.id</li>
                        </ul>
                    </div>
                </div>
                
                <div class="container copyright">
                    &copy; {{ current_year }} TechStore | UTS Cloud Computing
                </div>
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
