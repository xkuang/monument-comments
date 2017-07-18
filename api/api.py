from flask import Flask, jsonify, request
import psycopg2
import json


from psycopg2 import extras




app = Flask(__name__)


@app.route('/')
def root():
	return app.send_static_file('index.html')


@app.route('/document/<string:document_id>')
def return_document(document_id):
	conn = psycopg2.connect("dbname=comments user=postgres", cursor_factory=psycopg2.extras.RealDictCursor)
	cur = conn.cursor()
	query = """
		SELECT document_id, comment_text, posted_date, attachment_count
		FROM comments
		WHERE document_id = %s
		LIMIT 1;
	"""
	cur.execute(query, (document_id,))
	comment = cur.fetchone()
	conn.close()
	return jsonify(comment)

@app.route('/documents.json', methods=['GET', 'POST'])
def return_documents():
	params = request.get_json()
	if not params:
		return ('error - no json object supplied')


	conn = psycopg2.connect("dbname=comments user=postgres", cursor_factory=psycopg2.extras.RealDictCursor)
	cur = conn.cursor()
	args = list()

	#regexp_replace(document_id, '[\n\r]+', '<br />', 'g' ), 
	query = """
		SELECT document_id, 
		comment_text, posted_date, attachment_count
		FROM comments
		JOIN comment_entities ce ON comments.id = ce.comment_id
		JOIN entities ON entities.id = ce.entity_id
		JOIN entity_types et ON entities.type = et.type

		WHERE 
	"""
	where_count = 0

	for entity_type in params['entityTypes']:
		if where_count > 0:
			query += " OR "
		where_count += 1

		query += " et.type = %s "
		args.append(entity_type['type']) 
		query += " and entities.id IN ( "
		id_count = 0
		for id in entity_type['entityIds']:
			if id_count > 0:
				query += ","
			id_count += 1
			query += "%s"
			args.append(str(id))
		query += ") "

	if 'source' in params.keys():
		if where_count > 0:
			query += " AND "
		where_count += 1

		query += " source_type=%s "
		args.append(params['source'])


	if 'sentiment' in params.keys():
		if where_count > 0:
			query += " AND "
		where_count += 1

		query += " sentiment=%s "
		args.append(params['sentiment'])

	query += " LIMIT %s "
	if 'limit' in params.keys():
		args.append(params['limit'])
	else:
		args.append(25)

	if 'offset' in params.keys():
		query += " OFFSET %s "
		args.append(params['offset'])

	query += ";"

	cur.execute(query, args)
	comments = cur.fetchall()
	conn.close()

	return jsonify(comments)

@app.route('/entities.json')
def return_entities():
	conn = psycopg2.connect("dbname=comments user=postgres", cursor_factory=psycopg2.extras.RealDictCursor)
	cur = conn.cursor()
	args = list()

	query = """
		SELECT ent.cnt as count, id, name, type 
		FROM entities 
		JOIN (SELECT entity_id, COUNT(*) as cnt FROM comment_entities GROUP BY entity_id) ent ON ent.entity_id = entities.id
		ORDER BY name;
	"""
	cur.execute(query)
	entities = cur.fetchall()
	cur.execute("SELECT * FROM entity_types ORDER BY type;")
	entity_types = cur.fetchall()

	result = { 
		et['type']: {
			"name": et['name'],
			"values": [{ "id": entity['id'], "count": entity['count'], "name": entity['name'] } for entity in entities if entity['type'] == et['type'] ],
			"count": None
			}
		for et in entity_types }
	for key, value in result.items():
		result[key]['count'] = sum([entity['count'] for entity in value['values']])

	conn.close()
	return jsonify(result)