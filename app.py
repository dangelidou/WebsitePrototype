# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
import numpy as np


# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])

app.run(debug=True)
@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    try:
       
        search_name = request.args.get('name')
        if not search_name:
            return jsonify({"error": "Name parameter is required"}), 400
        results = mongo.db.products.find({"name": search_name}).sort("price", 1)
        result_list = []
        for result in results:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string
            result_list.append(result)
    
        return jsonify(result_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    try:
        data = request.get_json()
        
        if not all(k in data for k in ("id", "name", "production_year", "price", "color", "size")):
            return jsonify({"error": "Invalid input"}), 400

        # Check if color and size are in the required range
        if data['color'] not in [1, 2, 3] or data['size'] not in [1, 2, 3, 4]:
            return jsonify({"error": "Invalid color or size"}), 400
        
        new_product = {
            "id": data["id"],
            "name": data["name"],
            "production_year": data["production_year"],
            "price": data["price"],
            "color": data["color"],
            "size": data["size"]
        }

        result = mongo.db.products.replace_one(
            {"name": data["name"]},  # Filter to find the product by name
            new_product,  # New product data
            upsert=True  # Insert the document if it doesn't exist
        )
        
        if result.matched_count:
            message = "Product updated"
            status_code = 200
        else:
            message = "Product added"
            status_code = 201
        
        return jsonify({"message": message}), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    try:
        product_name = request.json.get("name")
        product = mongo.db.products.find_one({"name": product_name})
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        similarity_threshold = 0.7
        all_products = list(mongo.db.products.find())
    
        def extract_features(product):
            return np.array([product["production_year"], product["price"], product["color"], product["size"]])

        product_features = extract_features(product)
        all_features = np.array([extract_features(p) for p in all_products])

        def magnitude(feature_array):
            a = 0
            for feature in feature_array:
                a = a + np.square(feature)
            return np.sqrt(a)
        
        similar_product_names = []
        for i, f in enumerate(all_features):
            similarity = np.dot(product_features, f) / (magnitude(product_features) * magnitude(f))
            if similarity >= similarity_threshold and all_products[i]["name"] != product_name:
                similar_product_names.append(all_products[i]["name"])

        return jsonify(similar_product_names)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    
    try:
        semester = request.args.get('semester')
        url = "https://qa.auth.gr/el/x/studyguide/600000438/current"

        options = Options()
        options.headless = True

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        elementID = "exam" + str(semester)

        exam_element = driver.find_element(By.ID, elementID)
        tbody_element = exam_element.find_element(By.TAG_NAME, "tbody")

        rows = tbody_element.find_elements(By.TAG_NAME, "tr")
        course_titles = []
        for row in rows:
                course_title = row.get_attribute("coursetitle")
                if course_title:
                    course_titles.append(course_title)
                
        driver.quit()

        res = {"course_titles": course_titles}

        return res
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # END CODE HERE
