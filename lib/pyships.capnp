@0xd001427861034c3b;

struct Coord {
    x @0 :UInt8;
    y @1 :UInt8;
}

struct Ship {
    size @0 :UInt8;
    coords @1 :List(Coord);
}

interface PyShips {
	connect @0 () -> (id :UInt8);
	placeShip @1 (id :UInt8, ship :Ship);
	fire @2 (id :UInt8, coord :Coord) -> (hit :Bool);
}