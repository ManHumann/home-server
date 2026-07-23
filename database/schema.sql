-- schema.sql

DROP TABLE IF EXISTS images;

CREATE TABLE images(
	id	SERIAL PRIMARY KEY,
	original_filename	VARCHAR(255) NOT NULL,
	stored_filename		VARCHAR(255) NOT NULL,
	file_path		VARCHAR(255) NOT NULL,
	mime_type		VARCHAR(255) NOT NULL,
	file_size		BIGINT NOT NULL,
	uploaded_at		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
