import { useState } from 'react';
import { useParams } from 'react-router-dom';
import './ProdPage.css';

const prod = {
  id: 1,
  name: "Classic Polo",
  price: 4999,
  oldPrice: 6666,
  desc: "Premium polo shirt from 100% cotton. Good for office and casual.",
  imgs: ["/images/polo.jpg"],
  sizes: ["XS", "S", "M", "L", "XL"],
  colors: ["Black", "White", "Navy"],
  cat: "T-shirts",
  stars: 5,
  inStock: true
};

const ProdPage = () => {
  const { id } = useParams();
  const [size, setSize] = useState("M");
  const [qty, setQty] = useState(1);
  const [mainImg, setMainImg] = useState(prod.imgs[0]);
  
  const addToCart = () => {
    alert(`Added: ${prod.name}, Size: ${size}, Qty: ${qty}`);
  };

  return (
    <div className="prod">
      <div className="prod-main">
        <div className="prod-pics">
          <img src={mainImg} alt={prod.name} className="prod-big" />
          <div className="prod-small">
            {prod.imgs.map((img, i) => (
              <img 
                key={i} 
                src={img} 
                alt={`${prod.name} ${i + 1}`}
                onClick={() => setMainImg(img)}
                className={mainImg === img ? 'active' : ''}
              />
            ))}
          </div>
        </div>

        <div className="prod-info">
          <h1 className="prod-name">{prod.name}</h1>
          
          <div className="prod-price">
            <span className="prod-now">{prod.price.toLocaleString()}₽</span>
            {prod.oldPrice && (
              <span className="prod-old">{prod.oldPrice.toLocaleString()}₽</span>
            )}
          </div>

          <div className="prod-stars">
            {[...Array(5)].map((_, i) => (
              <i key={i} className={`fas fa-star ${i < prod.stars ? 'fill' : ''}`}></i>
            ))}
          </div>

          <p className="prod-text">{prod.desc}</p>

          <div className="prod-size">
            <h3>Size</h3>
            <div className="size-opt">
              {prod.sizes.map(s => (
                <button key={s} className={`size-btn ${size === s ? 'on' : ''}`} onClick={() => setSize(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div className="prod-qty">
            <h3>Quantity</h3>
            <div className="qty-box">
              <button onClick={() => setQty(q => q > 1 ? q - 1 : 1)}>-</button>
              <span>{qty}</span>
              <button onClick={() => setQty(q => q + 1)}>+</button>
            </div>
          </div>

          <div className="prod-btns">
            <button className="prod-btn-cart" onClick={addToCart}>
              Add to Cart
            </button>
            <button className="prod-btn-wish">
              <i className="far fa-heart"></i> Wish
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};

export default ProdPage;