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
  nomer int,
  dist text,
  districtid int
);

create table checkdistdistricts
(
  id int,
  name text,
  regionid text,
  regionname text,
  picname text,
  farmname
);
