action_score = importdata('scores\action_shot_score_all.mat');
face_score = importdata('scores\face_shot_score_all.mat');
action_index = action_score(:,1:2);
face_index = face_score(:, 1:2);

j=1;
index = [];
for i=1:length(face_index)
    if sum(abs((face_index(i, :) - action_index(j, :))))==0
        j = j + 1;
        continue;
    end
    index = [index, j];
    j = j + 2;  
end
action_score(index, :) = [];
save('scores/action_shot_score_all.mat', 'action_score');