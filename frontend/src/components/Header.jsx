import './Header.css';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useCart } from '../contexts/CartContext';

const Header = () => {
  const { user } = useAuth();
  const { cartCount } = useCart();
  
  return (
    <>
      <div className="sale-banner">
        <p>Discount on your first order 15%</p>
      </div>
      <header className="header">
        <div className="logo">
          <Link to="/">VERVE</Link>
        </div>
        
        <nav>
          <ul className="menu">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/catalog">Shop</Link></li>
            <li><Link to="/catalog?gender=women">Women</Link></li>
            <li><Link to="/catalog?gender=men">Men</Link></li>
            <li><Link to="/">About</Link></li>
          </ul>
        </nav>

        <div className="header-actions">
          <div className="search">
            <input type="text" placeholder="Search" />
            <button><i className="fas fa-search"></i></button>
          </div>
          
          <Link to={user ? "/profile" : "/login"}>
            <button className="icon-button" title={user ? "Profile" : "Login"}>
              <i className="fas fa-user"></i>
            </button>
          </Link>
          
          <Link to="/cart">
            <button className="icon-button" title="Cart">
              <i className="fas fa-shopping-bag"></i>
              {cartCount > 0 && (<span className="cart-badge">{cartCount}</span>)}
            </button>
          </Link>
          
          <Link to="/favorites">
            <button className="icon-button" title="Wishlist">
              <i className="far fa-heart"></i>
            </button>
          </Link>
        </div>
      </header>
    </>
  );
};

export default Header;