from database import SessionLocal
import models as models

db = SessionLocal()

print("--- Database Test Start ---")

# Clean up before
old_sponsors = db.query(models.Sponsor).filter_by(email="test_sponsor_xyz@example.com").all()
for os in old_sponsors:
    db.delete(os)

old_clients = db.query(models.Client).filter_by(email="test_client_xyz@example.com").all()
for oc in old_clients:
    db.delete(oc)
db.commit()

# Create a Sponsor
sponsor = models.Sponsor(
    name="Test Sponsor XYZ",
    email="test_sponsor_xyz@example.com",
    phone="123456789",
    status="active",
    notes="Test notes"
)
sponsor.set_password("testpass123")
db.add(sponsor)
db.commit()
db.refresh(sponsor)

print(f"Sponsor created with ID: {sponsor.id}")
print(f"Password verified: {sponsor.verify_password('testpass123')}")
print(f"Password fails on bad pass: {not sponsor.verify_password('wrong')}")

# Create a Client associated with this Sponsor
client = models.Client(
    name="Test Client XYZ",
    email="test_client_xyz@example.com",
    company="Test Company",
    phone="987654321",
    status="active",
    notes="Client notes",
    sponsor_id=sponsor.id
)
client.set_password("clientpass123")
db.add(client)
db.commit()
db.refresh(client)

print(f"Client created with ID: {client.id} linked to Sponsor ID: {client.sponsor_id}")
print(f"Client password verified: {client.verify_password('clientpass123')}")

# Test relationship
print(f"Sponsor has {len(sponsor.clients)} clients.")
assert sponsor.clients[0].email == "test_client_xyz@example.com", "Relationship check failed!"

print("Relationship test passed!")

# Clean up
db.delete(client)
db.delete(sponsor)
db.commit()
db.close()

print("--- Database Test End, All Passed! ---")
