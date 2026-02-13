import './Footer.css';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer>
      <div className="footer-content">
        <div className="footer-section">
          <h3>VERVE</h3>
          <p>A modern clothing store that combines<br />style and quality</p>
        </div>
        
        <div className="footer-section">
          <h4>Store</h4>
          <ul className="footer-links">
            <li><Link to="/catalog"><a>Women's clothing</a></Link></li>
            <li><Link to="/catalog"><a>Men's clothing</a></Link></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Support</h4>
          <ul className="footer-links">
            <li><a href="/">Questions</a></li>
            <li><a href="/">Return product</a></li>
            <li><a href="/">Write to support</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Contacts</h4>
          <ul className="contacts">
            <li><i className="fas fa-map-marker-alt"></i> Dolgoprudny, Pervomayskaya Street</li>
            <li><i className="fas fa-phone"></i> +7 (999) 999-99-99</li>
            <li><i className="fas fa-envelope"></i> info@verve-shop.ru</li>
          </ul>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; 2025 Verve</p>
      </div>
    </footer>
  );
};

export default Footer;