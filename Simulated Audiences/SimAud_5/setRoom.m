function room = setRoom( room, wallThickness, doorWidth)

[roomSizeY roomSizeX] = size(room);

%the outer walls
room(1:wallThickness, 1:roomSizeX) = 1;
room(roomSizeY-wallThickness:roomSizeY, 1:roomSizeX) = 1;
room(1:roomSizeY, 1:wallThickness) = 1;
room(1:roomSizeY, roomSizeX-wallThickness:roomSizeX) = 1;
%the door
room(roomSizeY/2-doorWidth/2:roomSizeY/2+doorWidth/2, 1:wallThickness) = 0;

%The sculpture
room (100:300, 300:350) = 1;

end

