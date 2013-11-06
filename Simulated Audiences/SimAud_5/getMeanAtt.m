function meanAtt = getMeanAtt( Att, attInFOV )

    [numAtt temp] = size(Att);
    [numAud temp] = size(attInFOV);
    meanAtt = zeros(numAud, 3);
   
    for i = 1:numAud
        numAttInFOV = 0;
        
        for j = 1:numAtt
            if (attInFOV (i,j) == 1)
                meanAtt(i,1:2) = meanAtt(i,1:2) + Att(j,:);
                numAttInFOV = numAttInFOV + 1;
            end
        end
        
        if (numAttInFOV > 0)
            meanAtt(i,1:2) = meanAtt(i,1:2)/numAttInFOV;
            meanAtt(i,3) = 1;
        end
    end

end

