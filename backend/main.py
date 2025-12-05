from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid
from datetime import datetime

app = FastAPI(title="Digital Fashion API", 
              description="Backend for Digital Fashion Platform - SIH 2024",
              version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Product(BaseModel):
    id: str
    name: str
    price: float
    category: str
    description: str
    water_saved: int
    co2_saved: int
    ai_generated: bool = False
    nft_ready: bool = True

class User(BaseModel):
    id: str
    name: str
    email: str
    wallet_address: Optional[str] = None

class NFTRequest(BaseModel):
    product_id: str
    user_id: str
    metadata: dict

class SustainabilityData(BaseModel):
    garment_type: str
    quantity: int = 1

# Mock database
products_db = []
users_db = []
nfts_db = []

@app.get("/")
def read_root():
    return {"message": "Digital Fashion API - SIH 2024", "status": "active"}

@app.get("/products", response_model=List[Product])
def get_products(category: Optional[str] = None):
    """Get all products, optionally filtered by category"""
    if category:
        return [p for p in products_db if p["category"] == category]
    return products_db

@app.post("/products")
def create_product(product: Product):
    """Add a new product"""
    products_db.append(product.dict())
    return {"message": "Product added", "id": product.id}

@app.get("/sustainability/calculate")
def calculate_sustainability(garment_type: str, quantity: int = 1):
    """Calculate environmental impact savings"""
    # Impact data per garment type
    impact_data = {
        't-shirt': {'water': 2700, 'co2': 10},
        'jeans': {'water': 7500, 'co2': 33},
        'dress': {'water': 5000, 'co2': 25},
        'jacket': {'water': 6000, 'co2': 28},
        'shoes': {'water': 8000, 'co2': 40}
    }
    
    impact = impact_data.get(garment_type, {'water': 3000, 'co2': 15})
    
    return {
        'garment_type': garment_type,
        'quantity': quantity,
        'water_saved': impact['water'] * quantity,
        'co2_saved': impact['co2'] * quantity,
        'real_world_equivalents': {
            'showers': (impact['water'] * quantity) / 60,
            'car_km': (impact['co2'] * quantity) * 2.5,
            'trees': (impact['co2'] * quantity) / 21.77
        }
    }

@app.post("/nft/mint")
def mint_nft(request: NFTRequest):
    """Mint a digital garment as NFT"""
    nft_id = str(uuid.uuid4())
    nft = {
        'id': nft_id,
        'product_id': request.product_id,
        'user_id': request.user_id,
        'token_id': f"0x{str(uuid.uuid4()).replace('-', '')}",
        'metadata': request.metadata,
        'minted_at': datetime.now().isoformat(),
        'network': 'Polygon Mumbai',
        'contract_address': '0xDigitalFashionContract'
    }
    nfts_db.append(nft)
    
    return {
        'message': 'NFT minted successfully',
        'nft': nft,
        'transaction': {
            'hash': f"0x{str(uuid.uuid4()).replace('-', '')}",
            'status': 'confirmed',
            'gas_used': '45000'
        }
    }

@app.get("/nft/{user_id}")
def get_user_nfts(user_id: str):
    """Get all NFTs for a user"""
    user_nfts = [nft for nft in nfts_db if nft['user_id'] == user_id]
    return {'user_id': user_id, 'nfts': user_nfts, 'count': len(user_nfts)}

@app.post("/ar/try-on")
async def ar_try_on(file: UploadFile = File(...), garment_id: str = None):
    """Process AR try-on request"""
    # In real implementation, this would process the image and apply AR
    content = await file.read()
    
    return {
        'status': 'success',
        'message': 'AR overlay applied',
        'original_filename': file.filename,
        'processed_size': len(content),
        'garment_applied': garment_id,
        'ar_preview_url': f"/preview/{str(uuid.uuid4())}.png"
    }

@app.get("/stats/global")
def get_global_stats():
    """Get global platform statistics"""
    return {
        'total_users': len(users_db),
        'total_products': len(products_db),
        'total_nfts': len(nfts_db),
        'total_water_saved': sum(p.get('water_saved', 0) for p in products_db) * 100,
        'total_co2_saved': sum(p.get('co2_saved', 0) for p in products_db) * 100,
        'platform_impact': {
            'water_saved_liters': 45200000,
            'co2_saved_kg': 301500,
            'digital_garments': 15284,
            'active_users': 5420
        }
    }

# Initialize with sample data
@app.on_event("startup")
def startup_event():
    # Sample products
    sample_products = [
        {
            'id': '1',
            'name': 'Eco-Glow Dress',
            'price': 29.99,
            'category': 'dress',
            'description': 'AI-generated sustainable dress',
            'water_saved': 3000,
            'co2_saved': 15,
            'ai_generated': True,
            'nft_ready': True
        },
        {
            'id': '2',
            'name': 'Digital Denim Jacket',
            'price': 39.99,
            'category': 'jacket',
            'description': 'Virtual denim jacket',
            'water_saved': 6000,
            'co2_saved': 28,
            'ai_generated': False,
            'nft_ready': True
        }
    ]
    
    for product in sample_products:
        products_db.append(product)
    
    # Sample user
    users_db.append({
        'id': 'sih_user_1',
        'name': 'SIH Participant',
        'email': 'sih@digitalfashion.com',
        'wallet_address': '0xSIH2024DigitalFashion'
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)