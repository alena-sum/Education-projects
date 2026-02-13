import { Link } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import './Cart.css';

const Cart = () => {
  const { cart, cartCount, cartTotal, updateQuantity, removeFromCart, clearCart } = useCart();

  const shippingCost = cartTotal > 3000 ? 0 : 500;

  if (cartCount === 0) {
    return (
      <div className="cart">
        <div className="cart-head">
          <h1>Cart</h1>
        </div>
        <div className="cart-empty">
          <p>Your cart is empty</p>
          <Link to="/catalog">
            <button className="cart-btn-shop">Shop Now</button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="cart">
      <div className="cart-head">
        <h1>Cart</h1>
        <p className="cart-sub">{cartCount} items</p>
      </div>

      <div className="cart-main">
        <div className="cart-items">
          {cart.map(item => (
            <div key={item.id} className="cart-item">
              <img src={item.image} alt={item.name} className="cart-img" />
              
              <div className="cart-info">
                <h3 className="cart-name">{item.name}</h3>
                <p className="cart-price">{item.price.toLocaleString()}₽</p>
              </div>

              <div className="cart-qty">
                <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
                <span>{item.quantity}</span>
                <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
              </div>

              <div className="cart-total">
                {(item.price * item.quantity).toLocaleString()}₽
              </div>

              <button 
                className="cart-remove"
                onClick={() => removeFromCart(item.id)}
              >
                ×
              </button>
            </div>
          ))}
        </div>

        <div className="cart-sum">
          <div className="sum-head">
            <h3>Order Summary</h3>
          </div>

          <div className="sum-row">
            <span>Items ({cartCount})</span>
            <span>{cartTotal.toLocaleString()}₽</span>
          </div>

          <div className="sum-row">
            <span>Shipping</span>
            <span>{shippingCost === 0 ? "Free" : "500₽"}</span>
          </div>

          <div className="sum-row total">
            <span>Total</span>
            <span>{(cartTotal + shippingCost).toLocaleString()}₽</span>
          </div>
          
          <Link to="/buy">
            <button className="sum-btn">Buy</button>
          </Link>
          
          <Link to="/catalog">
            <button className="sum-btn-cont">Continue Shopping</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Cart;