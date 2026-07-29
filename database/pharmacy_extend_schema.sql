-- Run inside existing pharmacy_db. This extends your current 5-table DB and seeds 1000 products.
CREATE TABLE IF NOT EXISTS roles(id SERIAL PRIMARY KEY, role_name VARCHAR(50) UNIQUE NOT NULL, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
INSERT INTO roles(role_name,description) VALUES ('ADMIN','System Administrator'),('CUSTOMER','Customer'),('MANAGER','Store Manager'),('PHARMACIST','Pharmacist') ON CONFLICT DO NOTHING;
CREATE TABLE IF NOT EXISTS users(id BIGSERIAL PRIMARY KEY, name VARCHAR(150), email VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255), role VARCHAR(30) DEFAULT 'CUSTOMER', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS categories(id BIGSERIAL PRIMARY KEY, name VARCHAR(200), slug VARCHAR(250) UNIQUE, icon VARCHAR(20), description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS brands(id BIGSERIAL PRIMARY KEY, name VARCHAR(200), slug VARCHAR(250) UNIQUE, logo_url TEXT, description TEXT, is_active BOOLEAN DEFAULT TRUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS products(id BIGSERIAL PRIMARY KEY, name VARCHAR(500), slug VARCHAR(500) UNIQUE, description TEXT, price NUMERIC(12,2) DEFAULT 0, sale_price NUMERIC(12,2), stock INT DEFAULT 0, image_url TEXT, category_id BIGINT REFERENCES categories(id), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
ALTER TABLE products ADD COLUMN IF NOT EXISTS sku VARCHAR(100) UNIQUE;
ALTER TABLE products ADD COLUMN IF NOT EXISTS brand_id BIGINT REFERENCES brands(id);
ALTER TABLE products ADD COLUMN IF NOT EXISTS mrp NUMERIC(12,2);
ALTER TABLE products ADD COLUMN IF NOT EXISTS rating NUMERIC(3,2) DEFAULT 4.4;
ALTER TABLE products ADD COLUMN IF NOT EXISTS reviews INT DEFAULT 0;
ALTER TABLE products ADD COLUMN IF NOT EXISTS ingredients TEXT;
ALTER TABLE products ADD COLUMN IF NOT EXISTS dosage TEXT;
ALTER TABLE products ADD COLUMN IF NOT EXISTS warnings TEXT;
ALTER TABLE products ADD COLUMN IF NOT EXISTS is_featured BOOLEAN DEFAULT FALSE;
ALTER TABLE products ADD COLUMN IF NOT EXISTS prescription_required BOOLEAN DEFAULT FALSE;
CREATE TABLE IF NOT EXISTS product_images(id BIGSERIAL PRIMARY KEY, product_id BIGINT REFERENCES products(id) ON DELETE CASCADE, image_url TEXT, is_primary BOOLEAN DEFAULT FALSE, display_order INT DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS inventory(id BIGSERIAL PRIMARY KEY, product_id BIGINT REFERENCES products(id) ON DELETE CASCADE, available_qty INT DEFAULT 0, reserved_qty INT DEFAULT 0, reorder_level INT DEFAULT 10, warehouse VARCHAR(200), updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS cart(id BIGSERIAL PRIMARY KEY, user_id BIGINT REFERENCES users(id) ON DELETE CASCADE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS cart_items(id BIGSERIAL PRIMARY KEY, cart_id BIGINT REFERENCES cart(id) ON DELETE CASCADE, product_id BIGINT REFERENCES products(id), quantity INT DEFAULT 1, unit_price NUMERIC(12,2), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS addresses(id BIGSERIAL PRIMARY KEY, user_id BIGINT REFERENCES users(id) ON DELETE CASCADE, full_name VARCHAR(150), phone VARCHAR(30), address_line1 TEXT, address_line2 TEXT, city VARCHAR(100), state VARCHAR(100), country VARCHAR(100) DEFAULT 'India', postal_code VARCHAR(20), is_default BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS orders(id BIGSERIAL PRIMARY KEY, order_number VARCHAR(50) UNIQUE, user_id BIGINT REFERENCES users(id), address_id BIGINT REFERENCES addresses(id), subtotal NUMERIC(12,2), tax_amount NUMERIC(12,2), shipping_amount NUMERIC(12,2), discount_amount NUMERIC(12,2), total NUMERIC(12,2), status VARCHAR(50) DEFAULT 'Processing', payment_status VARCHAR(50) DEFAULT 'Pending', payment_method VARCHAR(100), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_number VARCHAR(50) UNIQUE;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS total NUMERIC(12,2);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'Processing';
ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_status VARCHAR(50) DEFAULT 'Pending';
ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_method VARCHAR(100);
CREATE TABLE IF NOT EXISTS order_items(id BIGSERIAL PRIMARY KEY, order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE, product_id BIGINT REFERENCES products(id), quantity INT DEFAULT 1, price NUMERIC(12,2));
CREATE TABLE IF NOT EXISTS payments(id BIGSERIAL PRIMARY KEY, order_id BIGINT REFERENCES orders(id), transaction_id VARCHAR(200), payment_gateway VARCHAR(100), payment_method VARCHAR(100), amount NUMERIC(12,2), payment_status VARCHAR(50), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS reviews(id BIGSERIAL PRIMARY KEY, product_id BIGINT REFERENCES products(id) ON DELETE CASCADE, user_id BIGINT REFERENCES users(id), rating INT, title VARCHAR(200), review_text TEXT, is_approved BOOLEAN DEFAULT TRUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS wishlists(id BIGSERIAL PRIMARY KEY, user_id BIGINT REFERENCES users(id) ON DELETE CASCADE, product_id BIGINT REFERENCES products(id) ON DELETE CASCADE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(user_id,product_id));
CREATE TABLE IF NOT EXISTS coupons(id BIGSERIAL PRIMARY KEY, code VARCHAR(80) UNIQUE, discount_type VARCHAR(30), discount_value NUMERIC(12,2), start_date DATE, end_date DATE, usage_limit INT, is_active BOOLEAN DEFAULT TRUE);
CREATE TABLE IF NOT EXISTS audit_logs(id BIGSERIAL PRIMARY KEY, user_id BIGINT REFERENCES users(id), module_name VARCHAR(100), action_name VARCHAR(100), record_id BIGINT, old_value JSONB, new_value JSONB, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
INSERT INTO users(name,email,password,role) VALUES ('Admin','admin@pharmacy.test','$2a$10$2bclT6PEsQpIlhR3tzhhH.ZmefFnu72n6Fshd4fBPlyO4wa9fjB4S','ADMIN') ON CONFLICT(email) DO NOTHING;
INSERT INTO categories(name,slug,icon,description) VALUES
('OTC Medicines','otc-medicines','💊','Daily pharmacy essentials'),('Prescription Medicines','prescription-medicines','🧾','Doctor prescribed medicines'),('Baby Care','baby-care','🧴','Lotion wipes shampoo and infant care'),('Milk Powder','milk-powder','🍼','Infant formula and nutrition'),('Vitamins','vitamins','🍊','Vitamin wellness products'),('Supplements','supplements','🌿','Health supplements'),('Protein Products','protein-products','💪','Protein powder and bars'),('Healthcare Devices','healthcare-devices','🩺','Health monitoring devices'),('Personal Care','personal-care','🧼','Hygiene products'),('Beauty Products','beauty-products','✨','Skin essentials') ON CONFLICT(slug) DO NOTHING;
INSERT INTO brands(name,slug) VALUES ('Nestle','nestle'),('Abbott','abbott'),('PediaSure','pediasure'),('Johnson & Johnson','johnson-johnson'),('Himalaya','himalaya'),('Pampers','pampers'),('Dettol','dettol'),('Aptamil','aptamil'),('Ensure','ensure'),('Dabur','dabur'),('Cipla','cipla'),('Sun Pharma','sun-pharma') ON CONFLICT(slug) DO NOTHING;
INSERT INTO coupons(code,discount_type,discount_value,start_date,end_date,usage_limit,is_active) VALUES ('WELCOME10','PERCENT',10,current_date,current_date+365,1000,true),('BABY20','PERCENT',20,current_date,current_date+365,500,true),('HEALTH15','PERCENT',15,current_date,current_date+365,750,true) ON CONFLICT(code) DO NOTHING;
INSERT INTO products(name,slug,sku,description,price,sale_price,stock,image_url,category_id,brand_id,mrp,rating,reviews,ingredients,dosage,warnings,is_featured,prescription_required)
SELECT nm || ' ' || g, lower(regexp_replace(nm || '-' || g,'[^a-zA-Z0-9]+','-','g')), 'MED-'||lpad(g::text,5,'0'), 'Quality pharmacy product for family healthcare and wellness.', round((99+(g%650)+(g%9)*3.5)::numeric,2), CASE WHEN g%4=0 THEN round((89+(g%500))::numeric,2) ELSE NULL END, 20+(g%220), c.icon, c.id, b.id, round((129+(g%780))::numeric,2), round((3.5+((g%15)::numeric/10))::numeric,2), 5+(g%340), 'Approved ingredients as per product category.', CASE WHEN g%3=0 THEN 'Use only as directed by physician.' ELSE 'Use as mentioned on product label.' END, CASE WHEN g%4=0 THEN 'Prescription may be required. Keep away from children.' ELSE 'Store in a cool and dry place.' END, g<=48, c.slug='prescription-medicines'
FROM generate_series(1,1000) g
JOIN LATERAL (SELECT (ARRAY['Paracetamol 500mg','Dolo 650','Cetirizine','Vitamin C Sugarless','Vitamin D3 Capsule','Omega 3 Fish Oil','Multivitamin Complete','Whey Protein Chocolate','Protein Isolate Vanilla','Nestle NAN Optipro','Nestle Lactogen','Aptamil Gold Infant Formula','Similac Advance','PediaSure Vanilla','Johnson Baby Lotion','Johnson Baby Oil','Baby Shampoo Mild','Baby Wipes Pack','Himalaya Baby Cream','Dettol Hand Wash','Digital Thermometer','BP Monitor Digital','Pulse Oximeter','Face Wash Gentle','Sunscreen SPF 50','Herbal Liver Detox','Cough Syrup Honey','Antacid Gel','Pain Relief Spray','Calcium Tablets'])[1+(g%30)] nm) n ON true
JOIN categories c ON c.id = (SELECT id FROM categories ORDER BY id OFFSET ((g-1)%10) LIMIT 1)
JOIN brands b ON b.id = (SELECT id FROM brands ORDER BY id OFFSET ((g-1)%12) LIMIT 1)
ON CONFLICT(sku) DO NOTHING;
INSERT INTO inventory(product_id,available_qty,reserved_qty,reorder_level,warehouse) SELECT id, stock, 0, 10, 'Main Warehouse' FROM products ON CONFLICT DO NOTHING;
INSERT INTO product_images(product_id,image_url,is_primary,display_order) SELECT id, image_url, true, 1 FROM products ON CONFLICT DO NOTHING;
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand_id);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
