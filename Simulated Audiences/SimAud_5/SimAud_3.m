%% =====Initialization=======
clear;
%=====Attributes======
%number of audiences
numAud = 20;

%field of view (radian)
fov = degtorad(30);


%=====Initial values=======
%initial positions and angles
x0 = zeros(numAud, 1);
y0 = zeros(numAud, 1);
ang0 = zeros(numAud, 1);


%% =====Instantiation======
%SIMulated perSONs
SimSon = [x0 y0 ang0];

%things that attract the audiences' attention
numAtt = 2;
Att = zeros(numAtt, 2);
Att(1, :) = [300 30];
Att(2, :) = [300 120];

%Strength of the attractor
AttStr = 0.7;
%AttStr = zeros(numAtt, 1);
%AttStr(1, :) = 0.1;
%AttStr(2, :) = 0.1;

AngShift = zeros(numAud, 1);

%% =====Motion==========
%move the SimSon by one step
numStep = 250;
for i=1:numStep
    

    %find the attrractor that is closest to the SimSon
    %closestAtt = getClosestAtt(Att, SimSon);
    attInFOV = getAttInFOV(Att, SimSon, fov);
    
    meanAtt = getMeanAtt(Att, attInFOV);
    
   
    %calculate angle of the closet attractor relative to SimSon
   % AttAng = atan2(Att(closestAtt, 2)-SimSon(:,2), Att(closestAtt,1)-SimSon(:,1));
    AttAng = getAttInFOVAng(meanAtt(:, 1:2), SimSon);
    AngShift = meanAtt(:,3).*((AttAng (:, 1) -  SimSon(:,3))/2);
    SimSon = SimSonStep(SimSon, AngShift*AttStr);
  

%% ====Visualization========
plot(Att(:, 1), Att(:,2), 'bx');
hold on
%graph the audiences
plot(SimSon(:, 1),SimSon(:,2), 'ro');
axis([-50 350 -200 200]);
hold off


end




