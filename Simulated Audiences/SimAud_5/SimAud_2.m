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
Att(1, :) = [300 -120];
Att(2, :) = [300 120];

%Strength of the attractor
AttStr = zeros(numAtt, 1);
AttStr(1, :) = 0.1;
AttStr(2, :) = 0.1;

AngShift = zeros(numAud, 1);

%% =====Motion==========
%move the SimSon by one step
numStep = 300;
for i=1:numStep
    
    %calculate distance to each attractor
    AttDist = zeros(numAud,numAtt);
    for AttID = 1:numAtt
        AttDist(:, AttID) = sqrt((Att(AttID,1)-SimSon(:,1)).^2 + (Att(AttID,2)-SimSon(:,2)).^2);
    end
    %find the attractor that is closest to each SimSon
    
    [shortDist,closestAtt] = min(AttDist,[],2);
    
    %calculate angle of the closet attractor relative to SimSon
    AttAng = atan2(Att(closestAtt, 2)-SimSon(:,2), Att(closestAtt,1)-SimSon(:,1));
   
    AngShift = (AttAng (:, 1) -  SimSon(:,3))/2;
    SimSon = SimSonStep(SimSon, AngShift.*AttStr(closestAtt));
end    

%% ====Visualization========
plot(Att(:, 1), Att(:,2), 'bx');
hold on
%graph the audiences
plot(SimSon(:, 1),SimSon(:,2), 'ro');
axis([-50 350 -200 200]);
hold off







