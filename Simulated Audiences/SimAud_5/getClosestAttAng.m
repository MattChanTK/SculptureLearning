function AttAng = getClosestAttAng( Att, SimSon, index )

    %calculate angle of the attractor specified by index relative to SimSon
    AttAng = atan2(Att(index, 2)-SimSon(:,2), Att(index,1)-SimSon(:,1));

end

