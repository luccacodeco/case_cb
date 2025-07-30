-- Modelagem SQL para ERP.json

CREATE TABLE guest_checks (
    guest_check_id BIGINT PRIMARY KEY,
    chk_num INT NOT NULL,
    opn_bus_dt DATE NOT NULL,
    opn_utc TIMESTAMP NOT NULL,
    opn_lcl TIMESTAMP NOT NULL,
    clsd_bus_dt DATE NOT NULL,
    clsd_utc TIMESTAMP NOT NULL,
    clsd_lcl TIMESTAMP NOT NULL,
    last_trans_utc TIMESTAMP NOT NULL,
    last_trans_lcl TIMESTAMP NOT NULL,
    last_updated_utc TIMESTAMP NOT NULL,
    last_updated_lcl TIMESTAMP NOT NULL,
    clsd_flag BOOLEAN NOT NULL,
    gst_cnt INT NOT NULL,
    sub_ttl NUMERIC(12,2),
    non_txbl_sls_ttl NUMERIC(12,2),
    chk_ttl NUMERIC(12,2),
    dsc_ttl NUMERIC(12,2),
    pay_ttl NUMERIC(12,2),
    bal_due_ttl NUMERIC(12,2),
    rvc_num INT,
    ot_num INT,
    oc_num INT,
    tbl_num INT,
    tbl_name TEXT,
    emp_num INT,
    num_srvc_rd INT,
    num_chk_prntd INT
);

CREATE TABLE taxes (
    guest_check_id BIGINT REFERENCES guest_checks(guest_check_id),
    tax_num INT,
    txbl_sls_ttl NUMERIC(12,2),
    tax_coll_ttl NUMERIC(12,2),
    tax_rate NUMERIC(6,2),
    type INT,
    PRIMARY KEY (guest_check_id, tax_num)
);

CREATE TABLE detail_lines (
    guest_check_line_item_id BIGINT PRIMARY KEY,
    guest_check_id BIGINT REFERENCES guest_checks(guest_check_id),
    rvc_num INT,
    dtl_ot_num INT,
    dtl_oc_num INT,
    line_num INT,
    dtl_id INT,
    detail_utc TIMESTAMP,
    detail_lcl TIMESTAMP,
    last_update_utc TIMESTAMP,
    last_update_lcl TIMESTAMP,
    bus_dt DATE,
    ws_num INT,
    dsp_ttl NUMERIC(12,2),
    dsp_qty NUMERIC(12,2),
    agg_ttl NUMERIC(12,2),
    agg_qty NUMERIC(12,2),
    chk_emp_id BIGINT,
    chk_emp_num INT,
    svc_rnd_num INT,
    seat_num INT
);

CREATE TABLE menu_items (
    guest_check_line_item_id BIGINT REFERENCES detail_lines(guest_check_line_item_id),
    mi_num INT,
    mod_flag BOOLEAN,
    incl_tax NUMERIC(12,6),
    active_taxes TEXT,
    prc_lvl INT,
    PRIMARY KEY (guest_check_line_item_id)
);
