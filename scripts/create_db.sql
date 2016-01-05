CREATE TABLE "autonomous_system" (
  `asn`   INTEGER PRIMARY KEY,
	`name`   VARCHAR(100),
	`created_timestamp`	DATETIME,
	`modified_timestamp`	DATETIME,
  'verified_timestamp' DATETIME
);

CREATE TABLE "prefix" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
  `ip_version`	INTEGER,
	`status`	VARCHAR(64),
	`prefix`	VARCHAR(128),
	`next_hop_ip`	VARCHAR(64),
	`metric`	INTEGER,
	`local_pref`	INTEGER,
	`weight`	INTEGER,
	`as_path`	TEXT,
	`route_origin`	VARCHAR(64),
	`origin_asn`	INTEGER,
	`next_hop_asn`	INTEGER,
	`created_timestamp`	DATETIME,
	`modified_timestamp`	DATETIME,
  'verified_timestamp' DATETIME,
	FOREIGN KEY(`origin_asn`) REFERENCES `autonomous_system`(`asn`),
  FOREIGN KEY(`next_hop_asn`) REFERENCES `autonomous_system`(`asn`)
);
  CREATE INDEX prefix_idx ON prefix(prefix);
  CREATE INDEX origin_asn_idx ON prefix(origin_asn);
  CREATE INDEX next_hop_asn_idx ON prefix(next_hop_asn);
