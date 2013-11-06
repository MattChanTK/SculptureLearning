%% =====Initialization=======
clear;

%=====the room=========
roomSizeX = 400;
roomSizeY = 400;
wallThickness = 5;
doorWidth = 50;
%zero is empty and one is occupied
%clear room
room = zeros(roomSizeY, roomSizeX);
%set room
room = setRoom( room, wallThickness, doorWidth);



%=====Simulated Persons======
%number of audiences
numAud = 25;

%Space that each SimSon occupies
SimSonSize = 4;

%distance between SimSon
distBetSimSon = 20;

%field of view (radian)
fov = degtorad(30);

%initial positions and angles
x0 = (-numAud*distBetSimSon+1:distBetSimSon:0)'; %0* ones(numAud, 1);
y0 = roomSizeY/2 * ones(numAud, 1);
ang0 = zeros(numAud, 1);

% SIMulated perSONs
SimSon = [x0 y0 ang0];
IsInsideRoom = zeros (numAud, 1);
prevSimSon = zeros(numAud, 3);

%=====Attractors=======
%things that attract the audiences' attention
numAtt = 1;
Att = zeros(numAtt, 2);
Att(1, :) = [310 230];
%Att(2, :) = [310 260];
%Att(3, :) = [310 125];

%Std Var of attractors
%attStdVar = 0.1;

%Strength of the attractor
AttStr = 0.6;
%AttStr = zeros(numAtt, 1);
%AttStr(1, :) = 0.1;
%AttStr(2, :) = 0.1;


%shift of the mean
AngShift = zeros(numAud, 1);
%newNormDist = zeros(numAud, 2);

%distance which the SimSon is considered to be closed to Att
distSimSonToAtt = 100;

%% =====Motion==========
%move the SimSon by one step
numStep = 2000;
for i=1:numStep
    

    %find the attrractor that is closest to the SimSon
    %closestAtt = getClosestAtt(Att, SimSon);
    attInFOV = getAttInFOV(Att, SimSon, fov);
    
    meanAtt = getMeanAtt(Att, attInFOV);
    
   
   % calculate angle of the closet attractor relative to SimSon
   % AttAng = atan2(Att(closestAtt, 2)-SimSon(:,2), Att(closestAtt,1)-SimSon(:,1));
    AttAng = getAttInFOVAng(meanAtt(:, 1:2), SimSon);
    AngShift = meanAtt(:,3).*((AttAng (:, 1) -  SimSon(:,3))/2);
   % newNormDist = [AttAng*AttStr ones(numAud, 1)*attStdVar];
    IsCloseToAtt = sqrt((meanAtt(:,1)-SimSon(:,1)).^2 + (meanAtt(:,2)-SimSon(:,2)).^2)...
                  < distSimSonToAtt;
    if (IsCloseToAtt(10) ==1)
        temp = 1;
    end
    %check if the SimSon is inside the room
    IsInsideRoom = isInsideRoom(SimSon, [roomSizeX roomSizeY], wallThickness) ;
    
    %clear the previous obstacle marker
%     for SimSonID = 1:numAud
%         % if IsInsideRoom (SimSonID)
%              room(max(round(prevSimSon(SimSonID,2)-SimSonSize/2), 1):max(round(prevSimSon(SimSonID,2)+SimSonSize/2), 1), ...
%                   max(round(prevSimSon(SimSonID,1)-SimSonSize/2), 1):max(round(prevSimSon(SimSonID,1)+SimSonSize/2), 1)) = 0;
%         % end
%     end

    %clear room
    room = zeros(roomSizeY, roomSizeX);
    %set room
    room = setRoom( room, wallThickness, doorWidth);

    
    %SimSon moves
    [SimSon room] = SimSonStep(SimSon, AngShift*AttStr, IsInsideRoom, IsCloseToAtt, room, SimSonSize);
    
    

%     %add the new person as obstacle
%     for SimSonID = 1:numAud
%        % if IsInsideRoom (SimSonID)
%             room(max(round(SimSon(SimSonID,2)-SimSonSize/2), 1):max(round(SimSon(SimSonID,2)+SimSonSize/2),1), ...
%                  max(round(SimSon(SimSonID,1)-SimSonSize/2), 1):max(round(SimSon(SimSonID,1)+SimSonSize/2),1)) = 1;
%        % end
%     end
%     
    % copy where the SimSon was so we could remove the marker later
    prevSimSon = SimSon;

    %% ====Visualization========
    %draw the room
    figure(1);clf; hold on;
    image(100*(1-room));
    colormap(gray);
    axis([-50 max(roomSizeX, roomSizeY) 0 max(roomSizeX, roomSizeY)])

    plot(Att(:, 1), Att(:,2), 'gx', 'markers', 10);
    %hold on
    %graph the audiences
    plot(SimSon(:, 1),SimSon(:,2), 'ro', 'markers', 3);
    %axis([-50 350 -200 200]);
    hold off
    
   
end




