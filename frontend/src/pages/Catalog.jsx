import { useState } from 'react';
import { products } from '../data/products';
import './Catalog.css';
import { useCart } from '../contexts/CartContext';
import { useWishlist } from '../contexts/WishlistContext';
import { Link } from 'react-router-dom';

const Catalog = () => {
  const [filtered, setFiltered] = useState(products);
  const [cat, setCat] = useState('all');
  const [size, setSize] = useState('all');
  const [price, setPrice] = useState(50000);
  const [selectedColors, setSelectedColors] = useState([]);
  const { addToCart } = useCart();
  const { isInWishlist, toggleWishlist } = useWishlist();

  const cats = ['all', 'shirts', 'suits', 'basic', 'jackets', 'pants', 'dresses', 'shoes', 'accessories'];
  const sizes = ['All', 'XS', 'S', 'M', 'L', 'XL'];

  const selectColor = (colorName) => {
    setSelectedColors([colorName]);
  };

  const filter = () => {
    let result = [...products];

    if (cat !== 'all') {
      result = result.filter(p => p.category === cat);
    }

    if (size !== 'all') {
      result = result.filter(p => p.sizes.includes(size));
    }

    result = result.filter(p => p.price <= price);

    if (selectedColors.length > 0) {
        result = result.filter(p => {
        return selectedColors.some(selectedColor => 
            p.colors.some(productColor => 
            productColor.toLowerCase().includes(selectedColor.toLowerCase()))
        );
        });
    }
    setFiltered(result);
  };

  const reset = () => {
    setCat('all');
    setSize('all');
    setPrice(50000);
    setFiltered(products);
    setSelectedColors([]);
  };

  return (
    <div className="cat">
      <div className="cat-head">
        <h1>Shop</h1>
        <p className="sub">Discover our premium clothing collection</p>
      </div>

      <div className="cat-main">
        <div className="filters">
          <div className="f-sec">
            <h3>Categories</h3>
            <div className="f-opt">
              {cats.map(c => (
                <button
                  key={c}
                  className={`f-btn ${cat === c ? 'active' : ''}`}
                  onClick={() => setCat(c)}
                >
                  {c.charAt(0).toUpperCase() + c.slice(1)}
                </button>))}
            </div>
          </div>

          <div className="f-sec">
            <h3>Price</h3>
            <div className="price-slide">
              <input
                type="range"
                min="0"
                max="50000"
                value={price}
                onChange={(e) => setPrice(Number(e.target.value))}/>
              <div className="price-vals">
                <span>0₽</span>
                <span>{price.toLocaleString()}₽</span>
              </div>
            </div>
          </div>

          <div className="f-sec">
            <h3>Size</h3>
            <div className="size-opt">
              {sizes.map(s => (
                <button key={s} className={`size-btn ${size === s ? 'active' : ''}`} onClick={() => setSize(s)}>
                  {s}
                </button>))}
            </div>
          </div>

          <div className="f-sec">
            <h3>Color</h3>
            <div className="color-opt">
            <button className={`c-btn black ${selectedColors.includes('black') ? 'active' : ''}`}
              onClick={() => selectColor('black')}></button>
            <button className={`c-btn white ${selectedColors.includes('white') ? 'active' : ''}`}
              onClick={() => selectColor('white')}></button>
            <button className={`c-btn brown ${selectedColors.includes('brown') ? 'active' : ''}`}
              onClick={() => selectColor('brown')}></button>
            <button className={`c-btn blue ${selectedColors.includes('blue') ? 'active' : ''}`}
              onClick={() => selectColor('blue')}></button>
            <button className={`c-btn red ${selectedColors.includes('red') ? 'active' : ''}`}
              onClick={() => selectColor('red')}></button>
            </div>
          </div>

          <div className="f-btns">
            <button className="apply" onClick={filter}>
              Apply Filters
            </button>
            <button className="reset" onClick={reset}>
              Reset All
            </button>
          </div>
        </div>

        <div className="goods">
          <div className="sort">
            <select className="sort-sel">
              <option>First More Popular</option>
              <option>Price Low to High</option>
              <option>Price High to Low</option>
              <option>First More Newest</option>
            </select>
            <span className="count">
              {filtered.length} products
            </span>
          </div>

          <div className="grid">
            {filtered.map(p => (
                
                <div key={p.id} className="card">
                    {p.discount > 0 && <div className="badge">-{p.discount}%</div>}
                    <button 
                    className="wishlist-btn"
                    onClick={() => toggleWishlist(p)}
                    style={{
                        position: 'absolute',
                        top: '15px',
                        right: '15px',
                        background: '#ffffff',
                        border: 'none',
                        borderRadius: '50%',
                        width: '35px',
                        height: '35px',
                        cursor: 'pointer',
                        color: isInWishlist(p.id) ? '#9b2c2c' : '#000000'}}>
                    <i className={isInWishlist(p.id) ? "fas fa-heart" : "far fa-heart"}></i>
                    </button>
                    <img src={p.image} alt={p.name} className="card-img" />
                    <div className="stars">
                    {[...Array(5)].map((_, i) => (
                        <i key={i} className={`fas fa-star ${i < p.rating ? 'fill' : ''}`}></i>
                    ))}
                    </div>
                    <h3 className="card-name">{p.name}</h3>
                    
                    <div className="card-price">
                    <span className="now">{p.price.toLocaleString()}₽</span>
                    {p.oldPrice && <span className="old">{p.oldPrice.toLocaleString()}₽</span>}
                    </div>
                    
                    <div className="card-btns">
                    <button className="card-btn-cart" onClick={() => addToCart(p, 1)}>
                        To Cart
                    </button>
                    <Link to={`/product/${p.id}`}>
                        <button className="card-btn-view">View Details</button>
                    </Link>
                    </div>
                </div>))}
          </div>

          <div className="pages">
            <button className="page-btn">
              <i className="fas fa-chevron-left"></i>
            </button>
            <button className="page-btn active">1</button>
            <button className="page-btn">2</button>
            <button className="page-btn">3</button>
            <button className="page-btn">
              <i className="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Catalog;