

CREATE TABLE IF NOT EXISTS public.users
(
    id serial NOT NULL,
    last_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    middle_name character varying(100) COLLATE pg_catalog."default",
    phone_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
    chat_id bigint,
    avatar bytea,
    points integer DEFAULT 0,
    role character varying(20) COLLATE pg_catalog."default" NOT NULL DEFAULT 'student'::character varying,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_chat_id_key UNIQUE (chat_id),
    CONSTRAINT users_phone_number_key UNIQUE (phone_number)
);

CREATE TABLE IF NOT EXISTS public.completed_tests
(
    id serial NOT NULL,
    student_id integer,
    test_id integer,
    final_score integer NOT NULL,
    test_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT completed_tests_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.tests
(
    id serial NOT NULL,
    course character varying(100) COLLATE pg_catalog."default" NOT NULL,
    test_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    max_score integer NOT NULL,
    module character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tests_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.completed_tests
    ADD CONSTRAINT completed_tests_student_id_fkey FOREIGN KEY (student_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_completed_tests_student
    ON public.completed_tests(student_id);


ALTER TABLE IF EXISTS public.completed_tests
    ADD CONSTRAINT completed_tests_test_id_fkey FOREIGN KEY (test_id)
    REFERENCES public.tests (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;
CREATE INDEX IF NOT EXISTS idx_completed_tests_test
    ON public.completed_tests(test_id);

END;

CREATE TABLE IF NOT EXISTS public.shop_items
(
    id serial NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    price numeric(10, 2) NOT NULL,
    image bytea,
    category_id integer,
    quantity integer DEFAULT 0,
    CONSTRAINT shop_items_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.product_categories
(
    id serial NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT product_categories_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.shop_items
    ADD CONSTRAINT shop_items_category_id_fkey FOREIGN KEY (category_id)
    REFERENCES public.product_categories (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_shop_items_category
    ON public.shop_items(category_id);

END;