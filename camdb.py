import cv2
import sqlite3

# Database setup
db_filename = "main.db"
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB)")

# Frame capture
cap = cv2.VideoCapture(0)  # Open the default camera

ret, frame = cap.read()
if not ret:
    print("Error reading frame")
    exit()

# Encode as binary (you might choose a different encoding)
success, encoded_image = cv2.imencode('.jpg', frame)
image_bytes = encoded_image.tobytes()

# Store in the database
cursor.execute("INSERT INTO images (image) VALUES (?)", (image_bytes,))
conn.commit()

# Retrieve, decode, and display an image (example)
cursor.execute("SELECT image FROM images WHERE id = ?", (1,))  # Assuming an image with id 1
retrieved_data = cursor.fetchone()[0]
nparr = np.frombuffer(retrieved_data, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow("Retrieved Image", img)

# Cleanup
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
conn.close()
