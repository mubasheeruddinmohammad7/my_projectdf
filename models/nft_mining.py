"""
NFT Minting Module for Digital Fashion
Simulates NFT minting on Polygon blockchain
"""

import json
import random
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import uuid

@dataclass
class NFTMetadata:
    """Metadata for NFT"""
    name: str
    description: str
    image: str
    external_url: str = ""
    animation_url: str = ""
    attributes: List[Dict] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = []

@dataclass
class NFT:
    """NFT data structure"""
    token_id: str
    owner: str
    metadata: NFTMetadata
    contract_address: str
    network: str = "Polygon Mumbai"
    minted_at: str = None
    transaction_hash: str = None
    block_number: int = None
    token_standard: str = "ERC-721"
    
    def __post_init__(self):
        if self.minted_at is None:
            self.minted_at = datetime.now().isoformat()
        if self.transaction_hash is None:
            self.transaction_hash = self._generate_transaction_hash()
        if self.block_number is None:
            self.block_number = random.randint(1000000, 5000000)

    def _generate_transaction_hash(self):
        """Generate a simulated transaction hash"""
        data = f"{self.token_id}{self.owner}{self.minted_at}"
        return f"0x{hashlib.sha256(data.encode()).hexdigest()[:64]}"
    
    def to_dict(self):
        """Convert to dictionary"""
        result = asdict(self)
        result['metadata'] = asdict(self.metadata)
        return result
    
    def to_json(self):
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

class NFTMinter:
    """Main NFT minting class"""
    
    # Polygon Mumbai contract addresses (testnet)
    CONTRACT_ADDRESSES = {
        "digital_fashion": "0x88B48F654c30e99bc2e4A1559b4Df1aD93B6C5d6",
        "eco_collection": "0x742d35Cc6634C0532925a3b844Bc9e0E5C7b7a1a",
        "ai_fashion": "0x5AEDA56215b167893e80B4fE6450A7C1c2A0c0c8"
    }
    
    def __init__(self, network: str = "Polygon Mumbai"):
        self.network = network
        self.minted_nfts = []
        self._load_mock_data()
    
    def _load_mock_data(self):
        """Load some mock NFT data for demo"""
        mock_nfts = [
            NFT(
                token_id="0x1a2b3c4d5e6f7890",
                owner="0xSIH2024User1",
                metadata=NFTMetadata(
                    name="Eco-Glow Dress",
                    description="AI-generated sustainable dress with glow effects",
                    image="https://ipfs.io/ipfs/QmXyZ123/eco-dress.png",
                    attributes=[
                        {"trait_type": "Category", "value": "Dress"},
                        {"trait_type": "AI Generated", "value": "Yes"},
                        {"trait_type": "Water Saved", "value": "3000L"},
                        {"trait_type": "CO2 Prevented", "value": "15kg"},
                        {"trait_type": "Rarity", "value": "Rare"}
                    ]
                ),
                contract_address=self.CONTRACT_ADDRESSES["digital_fashion"],
                network=self.network
            ),
            NFT(
                token_id="0x2b3c4d5e6f7890a1",
                owner="0xSIH2024User2",
                metadata=NFTMetadata(
                    name="Solar Panel Hoodie",
                    description="Digital hoodie with animated solar panel patterns",
                    image="https://ipfs.io/ipfs/QmAbC456/solar-hoodie.png",
                    attributes=[
                        {"trait_type": "Category", "value": "Jacket"},
                        {"trait_type": "AI Generated", "value": "Yes"},
                        {"trait_type": "Water Saved", "value": "6000L"},
                        {"trait_type": "CO2 Prevented", "value": "28kg"},
                        {"trait_type": "Rarity", "value": "Epic"}
                    ]
                ),
                contract_address=self.CONTRACT_ADDRESSES["eco_collection"],
                network=self.network
            )
        ]
        self.minted_nfts.extend(mock_nfts)
    
    def generate_token_id(self) -> str:
        """Generate unique token ID"""
        return f"0x{hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:40]}"
    
    def create_metadata(self, product_data: Dict) -> NFTMetadata:
        """Create metadata from product data"""
        # Environmental impact attributes
        impact_attributes = []
        if 'water_saved' in product_data:
            impact_attributes.append({
                "trait_type": "Water Saved",
                "value": f"{product_data.get('water_saved', 0)}L",
                "display_type": "number"
            })
        
        if 'co2_saved' in product_data:
            impact_attributes.append({
                "trait_type": "CO2 Prevented",
                "value": f"{product_data.get('co2_saved', 0)}kg",
                "display_type": "number"
            })
        
        # Base attributes
        attributes = [
            {"trait_type": "Category", "value": product_data.get('category', 'Fashion')},
            {"trait_type": "AI Generated", "value": "Yes" if product_data.get('ai_generated', False) else "No"},
            {"trait_type": "Digital", "value": "Yes"},
            {"trait_type": "Sustainable", "value": "Yes"},
            {"trait_type": "Platform", "value": "Digital Fashion SIH 2024"},
            {"trait_type": "Collection", "value": "Clean & Green Technology"}
        ]
        
        # Add rarity
        rarity = self._calculate_rarity(product_data)
        attributes.append({"trait_type": "Rarity", "value": rarity})
        
        # Add impact attributes
        attributes.extend(impact_attributes)
        
        # Create IPFS image URL (simulated)
        ipfs_hash = hashlib.md5(product_data.get('name', '').encode()).hexdigest()[:16]
        image_url = f"https://ipfs.io/ipfs/Qm{ipfs_hash}/{product_data.get('name', 'garment').replace(' ', '')}.png"
        
        return NFTMetadata(
            name=product_data.get('name', 'Digital Fashion Item'),
            description=product_data.get('description', 'Sustainable digital fashion item') + 
                       f"\n\nThis digital garment saved {product_data.get('water_saved', 0)}L of water and " +
                       f"prevented {product_data.get('co2_saved', 0)}kg of CO2 emissions.",
            image=image_url,
            external_url="https://sih2024.digitalfashion.com",
            animation_url=image_url.replace('.png', '.mp4') if product_data.get('animated', False) else "",
            attributes=attributes
        )
    
    def _calculate_rarity(self, product_data: Dict) -> str:
        """Calculate rarity based on product features"""
        score = 0
        
        # AI generated items are rarer
        if product_data.get('ai_generated', False):
            score += 2
        
        # Higher environmental impact = rarer
        if product_data.get('water_saved', 0) > 5000:
            score += 1
        if product_data.get('co2_saved', 0) > 20:
            score += 1
        
        # Determine rarity level
        if score >= 4:
            return "Legendary"
        elif score >= 3:
            return "Epic"
        elif score >= 2:
            return "Rare"
        else:
            return "Common"
    
    def mint_nft(self, product_data: Dict, owner_address: str, 
                 collection: str = "digital_fashion") -> NFT:
        """Mint a new NFT"""
        
        # Generate token ID
        token_id = self.generate_token_id()
        
        # Create metadata
        metadata = self.create_metadata(product_data)
        
        # Create NFT
        nft = NFT(
            token_id=token_id,
            owner=owner_address,
            metadata=metadata,
            contract_address=self.CONTRACT_ADDRESSES.get(collection, self.CONTRACT_ADDRESSES["digital_fashion"]),
            network=self.network
        )
        
        # Store the NFT
        self.minted_nfts.append(nft)
        
        return nft
    
    def transfer_nft(self, token_id: str, from_address: str, to_address: str) -> bool:
        """Transfer NFT ownership"""
        for nft in self.minted_nfts:
            if nft.token_id == token_id and nft.owner == from_address:
                nft.owner = to_address
                return True
        return False
    
    def get_nfts_by_owner(self, owner_address: str) -> List[NFT]:
        """Get all NFTs owned by an address"""
        return [nft for nft in self.minted_nfts if nft.owner == owner_address]
    
    def get_nft_by_token_id(self, token_id: str) -> Optional[NFT]:
        """Get NFT by token ID"""
        for nft in self.minted_nfts:
            if nft.token_id == token_id:
                return nft
        return None
    
    def verify_ownership(self, token_id: str, owner_address: str) -> bool:
        """Verify NFT ownership"""
        nft = self.get_nft_by_token_id(token_id)
        return nft is not None and nft.owner == owner_address
    
    def get_collection_stats(self) -> Dict:
        """Get collection statistics"""
        total_nfts = len(self.minted_nfts)
        unique_owners = len(set(nft.owner for nft in self.minted_nfts))
        
        # Calculate total environmental impact
        total_water_saved = 0
        total_co2_saved = 0
        
        for nft in self.minted_nfts:
            for attr in nft.metadata.attributes:
                if attr["trait_type"] == "Water Saved":
                    try:
                        water = int(attr["value"].replace('L', ''))
                        total_water_saved += water
                    except:
                        pass
                elif attr["trait_type"] == "CO2 Prevented":
                    try:
                        co2 = int(attr["value"].replace('kg', ''))
                        total_co2_saved += co2
                    except:
                        pass
        
        return {
            "total_nfts": total_nfts,
            "unique_owners": unique_owners,
            "total_water_saved_liters": total_water_saved,
            "total_co2_saved_kg": total_co2_saved,
            "avg_water_per_nft": total_water_saved // max(total_nfts, 1),
            "avg_co2_per_nft": total_co2_saved // max(total_nfts, 1),
            "collections": list(self.CONTRACT_ADDRESSES.keys())
        }
    
    def generate_smart_contract_code(self) -> str:
        """Generate sample Solidity smart contract code"""
        return """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DigitalFashionNFT is ERC721, Ownable {
    uint256 private _tokenIdCounter;
    string private _baseTokenURI;
    
    // Environmental impact tracking
    struct FashionImpact {
        uint256 waterSaved;  // in liters
        uint256 co2Prevented; // in kg
        uint256 wasteReduced; // in kg
    }
    
    mapping(uint256 => FashionImpact) public tokenImpact;
    mapping(uint256 => string) public tokenMetadataURI;
    
    constructor() ERC721("DigitalFashionNFT", "DFNFT") {
        _baseTokenURI = "https://api.digitalfashion.com/metadata/";
    }
    
    function mintDigitalFashion(
        address to,
        uint256 waterSaved,
        uint256 co2Prevented,
        uint256 wasteReduced,
        string memory metadataHash
    ) public onlyOwner returns (uint256) {
        _tokenIdCounter++;
        uint256 newTokenId = _tokenIdCounter;
        
        _safeMint(to, newTokenId);
        
        // Store environmental impact
        tokenImpact[newTokenId] = FashionImpact({
            waterSaved: waterSaved,
            co2Prevented: co2Prevented,
            wasteReduced: wasteReduced
        });
        
        // Store metadata
        tokenMetadataURI[newTokenId] = string(
            abi.encodePacked(_baseTokenURI, metadataHash)
        );
        
        emit DigitalFashionMinted(newTokenId, to, waterSaved, co2Prevented);
        
        return newTokenId;
    }
    
    function getImpact(uint256 tokenId) public view returns (
        uint256 waterSaved,
        uint256 co2Prevented,
        uint256 wasteReduced
    ) {
        require(_exists(tokenId), "Token does not exist");
        FashionImpact memory impact = tokenImpact[tokenId];
        return (impact.waterSaved, impact.co2Prevented, impact.wasteReduced);
    }
    
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "Token does not exist");
        return tokenMetadataURI[tokenId];
    }
    
    function totalMinted() public view returns (uint256) {
        return _tokenIdCounter;
    }
    
    function totalWaterSaved() public view returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 1; i <= _tokenIdCounter; i++) {
            total += tokenImpact[i].waterSaved;
        }
        return total;
    }
    
    event DigitalFashionMinted(
        uint256 indexed tokenId,
        address indexed owner,
        uint256 waterSaved,
        uint256 co2Prevented
    );
}
"""
    
    def generate_verification_proof(self, token_id: str) -> Dict:
        """Generate verification proof for blockchain"""
        nft = self.get_nft_by_token_id(token_id)
        if not nft:
            return {"error": "NFT not found"}
        
        # Simulate blockchain proof
        proof_data = {
            "token_id": token_id,
            "owner": nft.owner,
            "contract_address": nft.contract_address,
            "network": nft.network,
            "block_number": nft.block_number,
            "transaction_hash": nft.transaction_hash,
            "verified_at": datetime.now().isoformat(),
            "verification_method": "Simulated Blockchain",
            "proof": f"0x{hashlib.sha256(f'{token_id}{nft.owner}{nft.transaction_hash}'.encode()).hexdigest()}",
            "explorer_url": f"https://mumbai.polygonscan.com/tx/{nft.transaction_hash}"
        }
        
        return proof_data

# Example usage
def demo_nft_minting():
    """Demo the NFT minting functionality"""
    print("🚀 Digital Fashion NFT Minting Demo")
    print("=" * 50)
    
    # Initialize minter
    minter = NFTMinter()
    
    # Sample product data
    product_data = {
        "name": "Eco-Glow Dress",
        "description": "AI-generated sustainable dress with glow effects",
        "category": "Dress",
        "water_saved": 3000,
        "co2_saved": 15,
        "ai_generated": True,
        "animated": True
    }
    
    # Mint NFT
    print("\n1. Minting NFT...")
    owner_address = "0xSIH2024DemoUser"
    nft = minter.mint_nft(product_data, owner_address)
    
    print(f"✅ NFT Minted Successfully!")
    print(f"   Token ID: {nft.token_id}")
    print(f"   Owner: {nft.owner}")
    print(f"   Network: {nft.network}")
    print(f"   Contract: {nft.contract_address}")
    
    # Display metadata
    print("\n2. NFT Metadata:")
    print(json.dumps(nft.metadata.attributes, indent=2))
    
    # Verify ownership
    print("\n3. Verifying Ownership...")
    is_owner = minter.verify_ownership(nft.token_id, owner_address)
    print(f"   Ownership Verified: {is_owner}")
    
    # Generate verification proof
    print("\n4. Blockchain Verification Proof:")
    proof = minter.generate_verification_proof(nft.token_id)
    print(f"   Transaction Hash: {proof['transaction_hash']}")
    print(f"   Explorer URL: {proof['explorer_url']}")
    
    # Collection stats
    print("\n5. Collection Statistics:")
    stats = minter.get_collection_stats()
    print(f"   Total NFTs: {stats['total_nfts']}")
    print(f"   Unique Owners: {stats['unique_owners']}")
    print(f"   Total Water Saved: {stats['total_water_saved_liters']:,}L")
    print(f"   Total CO2 Prevented: {stats['total_co2_saved_kg']:,}kg")
    
    # Display smart contract code
    print("\n6. Sample Smart Contract Code (Solidity):")
    contract_code = minter.generate_smart_contract_code()
    print("   (Smart contract code generated - suitable for Polygon deployment)")
    
    return nft

if __name__ == "__main__":
    # Run demo
    demo_nft_minting()