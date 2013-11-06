function closestAtt = getClosestAtt(Att, SimSon)

    [numAud temp] = size(SimSon);
    [numAtt temp] = size(Att);
    
    %calculate distance to each attractor
    AttDist = zeros(numAud,numAtt);
    for AttID = 1:numAtt
        AttDist(:, AttID) = sqrt((Att(AttID,1)-SimSon(:,1)).^2 + (Att(AttID,2)-SimSon(:,2)).^2);
    end
    %find the attractor that is closest to each SimSon
    [temp,closestAtt] = min(AttDist,[],2);
    
end

