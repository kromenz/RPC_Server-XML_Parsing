CREATE TABLE public.documents (
	id              serial PRIMARY KEY,
	file_name       VARCHAR(250) UNIQUE NOT NULL,
	xml             XML NOT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	deleted_on      TIMESTAMP DEFAULT NULL
);

CREATE UNIQUE INDEX document_filename ON documents (file_name) WHERE deleted_on IS NULL;