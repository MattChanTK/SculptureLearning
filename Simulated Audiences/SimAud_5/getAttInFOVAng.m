function AttAng = getAttInFOVAng( meanAtt, SimSon )

    %calculate angle of the attractor specified by index relative to SimSon
    AttAng = atan2(meanAtt(:, 2)-SimSon(:,2), meanAtt(:,1)-SimSon(:,1));

end

