import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const { user, logout: authLogout, updateUser } = useAuth();
  const [edit, setEdit] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: ''
  });

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    
    setFormData({
      name: user.name || '',
      email: user.email || '',
      phone: user.phone || '',
      address: user.address || ''
    });
  }, [user, navigate]);

  const handleSave = () => {
    updateUser(formData);
    setEdit(false);
    alert('Profile updated successfully!');
  };

  const handleLogout = () => {
    authLogout();
    navigate('/login');
  };

  return (
    <div className="prof">
      <div className="prof-head">
        <h1>Welcome, {user.name}!</h1>
      </div>

      <div className="prof-main">
        <div className="prof-card">
          <div className="prof-card-head">
            <h2>Profile</h2>
            {!edit ? (
              <button className="prof-edit" onClick={() => setEdit(true)}>
                Edit
              </button>
            ) : (
              <div className="prof-btns">
                <button className="prof-save" onClick={handleSave}>
                  Save
                </button>
                <button className="prof-cancel" onClick={() => {
                  setEdit(false);
                  setFormData({
                    name: user.name || '',
                    email: user.email || '',
                    phone: user.phone || '',
                    address: user.address || ''
                  });
                }}>
                  Cancel
                </button>
              </div>
            )}
          </div>

          <div className="prof-info">
            <div className="prof-field">
              <label>Name</label>
              {edit ? (
                <input type="text" value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}/>) : (<p>{user.name}</p>)}
            </div>

            <div className="prof-field">
              <label>Email</label>
              {edit ? (<input type="email" value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}/>) : (<p>{user.email}</p>)}
            </div>

            <div className="prof-field">
              <label>Phone</label>
              {edit ? (<input type="tel" value={formData.phone}
                onChange={(e) => setFormData({...formData, phone: e.target.value})}/>) : (<p>{user.phone || 'Not set'}</p>)}
            </div>

            <div className="prof-field">
              <label>Address</label>
              {edit ? (
                <textarea
                  value={formData.address}
                  onChange={(e) => setFormData({...formData, address: e.target.value})}/>) : (
                  <p>{user.address || 'Not set'}</p>)}
            </div>
          </div>

          <button className="prof-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>

        <div className="prof-card">
          <h2>My Orders</h2>
          
          <p className="prof-no">No orders yet</p>
          
          <Link to="/catalog" className="prof-shop">
            Continue Shopping
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Profile;