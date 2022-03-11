#
# A simple endpoint that can receive documents from an external source, mark them up and return them.  This can be useful
# for hooking in callback functions during indexing to do smarter things like classification
#
from flask import (
    Blueprint, request, abort, current_app, jsonify
)
import fasttext
import json
from nltk import word_tokenize


bp = Blueprint('documents', __name__, url_prefix='/documents')

# Take in a JSON document and return a JSON document
@bp.route('/annotate', methods=['POST'])
def annotate():
    if request.mimetype == 'application/json':
        the_doc = request.get_json()
        response = {}
        cat_model = current_app.config.get("cat_model", None) # see if we have a category model
        syns_model = current_app.config.get("syns_model", None) # see if we have a synonyms/analogies model
        # We have a map of fields to annotate.  Do POS, NER on each of them
        sku = the_doc["sku"]
        for item in the_doc:
            the_text = the_doc[item]
            if the_text is not None and the_text.find("%{") == -1:
                if item == "name":
                    print("hitting nmae")
                    if syns_model is not None:
                        print("hitting syn model")

                        parts = word_tokenize(the_text)
                        syns_ret = []

                        for p in parts:
                            clean_p = p.strip().lower()
                            syns = syns_model.get_nearest_neighbors(clean_p, k=20)

                            for score,s in syns:
                                if score > 0.9:
                                    if s not in syns_ret:
                                        syns_ret.append(s)

                        print("sending rets" + str(syns_ret)   )         
                        response['name_synonyms'] = syns_ret

        return jsonify(response)
    abort(415)
