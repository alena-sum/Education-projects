import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Buy.css';

const Buy = () => {
  const navigate = useNavigate();
  const [isLogged, setIsLogged] = useState(false);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    name: '',
    email: '',
    address: '',
    card: ''
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      setIsLogged(true);
      const userData = JSON.parse(user);
      setForm(prev => ({
        ...prev,
        name: userData.name || '',
        email: userData.email || ''
      }));
    } else {
      if (window.confirm('Need to login first. Go to Login page?')) {
        navigate('/login');
      } else {
        navigate('/cart');
      }
    }
    setLoading(false);
  }, [navigate]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Order confirmed! Thanks, ${form.name}!`);
    navigate('/');
  };

  const items = [
    { name: "Classic Polo", qty: 1, price: 4999 },
    { name: "White T-shirt", qty: 2, price: 2999 }
  ];

  const total = items.reduce((sum, item) => sum + (item.price * item.qty), 0);

  if (loading) {
    return <div className="buy">Loading...</div>;
  }

  if (!isLogged) {
    return <div className="buy">Redirecting to login...</div>;
  }

  return (
    <div className="buy">
      <div className="buy-head">
        <h1>Placing Order</h1>
        <p className="buy-sub">Complete your order</p>
      </div>

      <div className="buy-main">
        <form onSubmit={handleSubmit} className="buy-form">
          <h2>Contact Info</h2>
          
          <div className="buy-field">
            <label>Name</label>
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              required/>
          </div>
          
          <div className="buy-field">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required/>
          </div>
          
          <div className="buy-field">
            <label>Address</label>
            <input
              type="text"
              name="address"
              value={form.address}
              onChange={handleChange}
              required/>
          </div>
          
          <h2>Payment</h2>
          
          <div className="buy-field">
            <label>Card Number</label>
            <input
              type="text"
              name="card"
              value={form.card}
              onChange={handleChange}
              placeholder="1234 5678 9012 3456"
              required/>
          </div>
          
          <button type="submit" className="buy-btn">
            Place Order - {total.toLocaleString()}₽
          </button>
        </form>

        <div className="buy-side">
          <h3>Your Order</h3>
          
          <div className="buy-items">
            {items.map((item, i) => (
              <div key={i} className="buy-item">
                <span>{item.name} ×{item.qty}</span>
                <span>{(item.price * item.qty).toLocaleString()}₽</span>
              </div>
            ))}
          </div>
          
          <div className="buy-tot">
            <div className="buy-row">
              <span>Items</span>
              <span>{total.toLocaleString()}₽</span>
            </div>
            <div className="buy-row">
              <span>Shipping</span>
              <span>Free</span>
            </div>
            <div className="buy-row total">
              <span>Total</span>
              <span>{total.toLocaleString()}₽</span>
            </div>
          </div>
          
          <Link to="/cart" className="buy-back">
            Back to Cart
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Buy;