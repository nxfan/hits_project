create table players (
    playerid varchar(20) primary key,
    playername varchar(40),
    weight integer,
    height integer,
    age integer
)

create table hits (
    Eventid integer primary key,
    playerid varchar(20),
    primaryposition varchar(30),
    impacttime timestamp,
    linearforce decimal,
    rotationalforce decimal
)

create view numhits as 
    select p.playerid, count(*)
    from hits h, players p
    where h.playerid = p.playerid
    group by p.playerid;

select p.playerid, c.impacttime, p.height, p.weight, c.linearforce, c.rotationalforce, c.impacttime - lag(c.impacttime) over (partition by p.playerid order by c.impacttime asc) as timedelta
from players p, hits c
where p.playerid = c.playerid
group by p.playerid, c.impacttime, c.linearforce, c.rotationalforce
order by p.playerid asc, c.impacttime asc;

select * from hits where extract(year from impacttime)=2017
and extract(month from impacttime) = 7
and extract(day from impacttime)=12
and extract (hour from impacttime) = 12
nxfan-> and extract (minute from impacttime) = 36;