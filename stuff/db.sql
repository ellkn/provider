CREATE DATABASE provider
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

BEGIN;


CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    email text,
    password text,
    lastname text,
    firstname text,
    phone text,
    role integer,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.roles
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    role text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.category
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    category text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.status
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    status text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.orders
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    user_id integer,
    good_id integer,
    datetime timestamp without time zone,
    status integer,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.banks
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    bank text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.info
(
    id integer,
    bank integer,
    client integer
);

CREATE TABLE IF NOT EXISTS public.goods
(
    "id " integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name text,
    price money,
    category integer,
    prov integer,
    PRIMARY KEY ("id ")
);

ALTER TABLE IF EXISTS public.users
    ADD CONSTRAINT role FOREIGN KEY (role)
    REFERENCES public.roles (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT "user" FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT status FOREIGN KEY (status)
    REFERENCES public.status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.orders
    ADD CONSTRAINT good FOREIGN KEY (good_id)
    REFERENCES public.goods ("id ") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.info
    ADD CONSTRAINT bank FOREIGN KEY (bank)
    REFERENCES public.banks (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.info
    ADD CONSTRAINT client FOREIGN KEY (client)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.goods
    ADD CONSTRAINT category FOREIGN KEY (category)
    REFERENCES public.category (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.goods
    ADD CONSTRAINT prov FOREIGN KEY (prov)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;



-- ЗАПОЛНЕНИЕ
INSERT INTO public.users (email, password, lastname, firstname, phone, role) VALUES ('11@1.1'::text, 'pbkdf2:sha1:260000$OMVHHXfS$cd3aea4ab64f688e2c4e8cd70ac1d24650dbb942'::text, 'admin'::text, 'admin'::text, '7909-909-90-90'::text, '1'::integer) returning id;

INSERT INTO public.roles (role) VALUES ('ADMIN'::text) returning id;
INSERT INTO public.roles (role) VALUES ('PROVIDER'::text) returning id;
INSERT INTO public.roles (role) VALUES ('USER'::text) returning id;


INSERT INTO public.status (status) VALUES ('OPEN'::text) returning id;
INSERT INTO public.status (status) VALUES ('CANCELED'::text) returning id;
INSERT INTO public.status (status) VALUES ('CLOSED'::text) returning id;
