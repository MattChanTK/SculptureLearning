function isInsideRoom = isInsideRoom( SimSon, roomDim, wallThickness )

isInsideRoom = SimSon(:, 1) > wallThickness + 10 &...
             SimSon(:, 1) < roomDim(:, 1) - wallThickness & ...
             SimSon(:, 2) > wallThickness &...
             SimSon(:, 2) < roomDim(:, 2) - wallThickness ;


end

