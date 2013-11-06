function  [newSimSon newRoom] = SimSonStep(SimSon, meanShift, isInsideRoom, isCloseToAtt, Room, SimSonSize)

[numAud temp] = size(SimSon);

%nominal distance per step
stepLength = 0.6;
% new step length
stdDev_step = 1.0;
step = random('norm', stepLength, stdDev_step);

%Gap before obstacle
gap = 10;

%num of trial (of rotating) before giving up
numTrials = 10;

% new facing angle
stdDev_rot = 0.08;
ang = random('norm', SimSon(:,3) + meanShift, stdDev_rot );


% move in the direction of new angle
x = SimSon(:, 1) + step*cos(ang).*isInsideRoom + stepLength*(1-isInsideRoom);
y = SimSon(:, 2) + step*sin(ang).*isInsideRoom;



for i=1:numAud
    
    
    % check if the new position is empty
    trial = 0;
    while (trial<numTrials)
    
        if isInsideRoom(i) &&...
           sum(sum(Room(max(round(y(i))- gap, 1):max(round(y(i))+ gap, 1),...
                           max(round(x(i))- gap, 1):max(round(x(i))+ gap, 1)))) > 0
            
            trial = trial + 1;
            
            if ~isCloseToAtt(i)
                ang(i) = random('norm', ang(i)+ pi/8, stdDev_rot );
            else
               
                trial = numTrials;
            end
            
            %if it is not empty
            x(i) = SimSon(i, 1) + step*cos(ang(i))*~isCloseToAtt(i);
            y(i) = SimSon(i, 2) + step*sin(ang(i))*~isCloseToAtt(i);
           

        else
        %if it is empty
            %add the new person as obstacle
            if isInsideRoom (i) 
               Room(round(y(i)-SimSonSize/2):round(y(i)+SimSonSize/2), ...
                    round(x(i)-SimSonSize/2):round(x(i)+SimSonSize/2)) = 1;
            end
            
            break;
        end

    end
    
    %set the old person as obtacle
     if isInsideRoom (i)
            Room(round(SimSon(i,2)-SimSonSize/2):round(SimSon(i,2)+SimSonSize/2), ...
                 round(SimSon(i,1)-SimSonSize/2):round(SimSon(i,1)+SimSonSize/2)) = 1;
     end

    
end


newSimSon = [x y ang];
newRoom = Room;

end

