import { Link } from 'react-router-dom';
import { useWishlist } from '../contexts/WishlistContext';
import { useCart } from '../contexts/CartContext';
import './Fav.css';

const Fav = () => {
  const { wishlist, removeFromWishlist, moveToCart } = useWishlist();
  const cartContext = useCart();

  const handleMoveToCart = (item) => {
    moveToCart(item, cartContext);
  };

  return (
    <div className="fav">
      <div className="fav-head">
        <h1>Wishlist</h1>
        <p className="fav-sub">{wishlist.length} items</p>
      </div>

      {wishlist.length === 0 ? (
        <div className="fav-empty">
          <p>Your wishlist is empty</p>
          <Link to="/catalog">
            <button className="fav-btn">Browse Catalog</button>
          </Link>
        </div>
      ) : (
        <div className="fav-grid">
          {wishlist.map(item => (
            <div key={item.id} className="fav-card">
              <Link to={`/product/${item.id}`}>
                <img src={item.image} alt={item.name} className="fav-img" />
              </Link>
              
              <div className="fav-info">
                <h3 className="fav-name">{item.name}</h3>
                
                <div className="fav-price">
                  <span className="fav-now">{item.price.toLocaleString()}₽</span>
                </div>
              </div>
              
              <div className="fav-btns">
                <button 
                  className="fav-btn-cart"
                  onClick={() => handleMoveToCart(item)}
                >
                  Add to Cart
                </button>
                <button 
                  className="fav-btn-remove"
                  onClick={() => removeFromWishlist(item.id)}
                >
                  <i className="fas fa-times"></i>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Fav;