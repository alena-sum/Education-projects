import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Login.css';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (isLogin) {
      if (form.email === 'info@verve-shop.ru' && form.password === '123456') {
        login(
          { 
            name: 'Admin', 
            email: form.email,
            phone: '+7 (999) 999-99-99',
            address: 'Dolgoprudny, Pervomayskaya Street'
          },
        );
        navigate('/profile');
      } else {
        setError('Incorrect email or password');
      }
    } else {
      login(
        { 
          name: form.name, 
          email: form.email,
          phone: '',
          address: ''
        },
      );
      navigate('/profile');
    }
  };

  return (
    <div className="login">
      <div className="login-box">
        <h1 className="login-title">{isLogin ? 'Authorization' : 'Registration'}</h1>
        
        {error && <div style={{ color: '#9b2c2c', marginBottom: '15px' }}>{error}</div>}
        
        <form onSubmit={handleSubmit} className="login-form">
          {!isLogin && (
            <div className="login-field">
              <label>Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({...form, name: e.target.value})}
                required/>
            </div>
          )}
          
          <div className="login-field">
            <label>Email</label>
            <input
              type="email"
              value={form.email}
              onChange={(e) => setForm({...form, email: e.target.value})}
              required/>
          </div>
          
          <div className="login-field">
            <label>Password</label>
            <input
              type="password"
              value={form.password}
              onChange={(e) => setForm({...form, password: e.target.value})}
              required/>
          </div>
          
          {!isLogin && (
            <div className="login-field">
              <label>Confirm Password</label>
              <input
                type="password"
                value={form.confirmPassword}
                onChange={(e) => setForm({...form, confirmPassword: e.target.value})}
                required/>
            </div>
          )}
          
          <button type="submit" className="login-btn">
            {isLogin ? 'Login' : 'Register'}
          </button>
        </form>
        
        <div className="login-switch">
          {isLogin ? "No account? " : "Have account? "}
          <button
            type="button"
            className="login-switch-btn"
            onClick={() => {
              setIsLogin(!isLogin);
              setError('');
            }}>
            {isLogin ? 'Register' : 'Login'}
          </button>
        </div>

      </div>
    </div>
  );
};

export default Login;