create table regions
(
  id int,
  kn text,
  name text
);

create table districts
(
  id int,
  kn text,
  name text,
  regionkn text,
  picname text
);

create table points
(
  id int,
  nomer int,
  status text,
  picr text,
  picg text,
  farmname text,
  districtid int
);

create table distances
(
  id int,
  nomer int,
  dist text,
  picr text,
  farmname text,
  districtid int
);
