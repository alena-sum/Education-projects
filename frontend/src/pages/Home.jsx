import './Home.css';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home">
      <div className="hero">
        <p className="hero-title">Your life. Your style<br />Your verve.</p>
        <Link to="/catalog">
        <button className="dark-button">Shop Now</button>
        </Link>
      </div>

      <div className="benefits">
        <div className="benefit">
          <div><i className="fas fa-shipping-fast"></i></div>
          <h3>Free shipping</h3>
          <p>For orders over 3000₽</p>
        </div>
        
        <div className="benefit">
          <div><i className="fas fa-exchange-alt"></i></div>
          <h3>Easy return</h3>
          <p>30 days for return</p>
        </div>
        
        <div className="benefit">
          <div><i className="fas fa-lock"></i></div>
          <h3>Secure payment</h3>
          <p>All payments are protected</p>
        </div>
        
        <div className="benefit">
          <div><i className="fas fa-headset"></i></div>
          <h3>Support 24/7</h3>
          <p>All-day assistance</p>
        </div>
      </div>

      <div className="top-products">
        <p className="section-title">Top Products</p>
        <p className="section-subtitle">The most popular products of the last week</p>

        <div className="products-grid">
          <div className="product">
            <div className="badge">-25%</div>
            <div className="product-image">
              <img src="/images/polo.jpg" alt="Polo" />
            </div>
            <div className="rating">
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
            </div>
            <h3>Classic Polo</h3>
            <div className="price">
              <div>4 999₽ <span>6 666₽</span></div>
            </div>
            <button className="add-to-cart">To Cart</button>
          </div>
          
          <div className="product">
            <div className="product-image">
              <img src="/images/tvid-costume.jpg" alt="Tvid suit" />
            </div>
            <div className="rating">
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
            </div>
            <h3>Tweed suit</h3>
            <div className="price">
              <div>14 999₽</div>
            </div>
            <button className="add-to-cart">To Cart</button>
          </div>
          
          <div className="product">
            <div className="badge">-10%</div>
            <div className="product-image">
              <img src="/images/t-shirt.jpg" alt="T-shirt" />
            </div>
            <div className="rating">
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
              <i className="fas fa-star"></i>
            </div>
            <h3>White T-shirt</h3>
            <div className="price">
              <div>2 999₽ <span>3 333₽</span></div>
            </div>
            <button className="add-to-cart">To Cart</button>
          </div>
        </div>

        <div className="view-all">
          <a href="/catalog">
            <button className="dark-button">View All</button>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Home;