%load probe_feature
probe_feat_dir = 'feature\global\probe\';
gallery_feat_dir = 'feature\global\gallery\';

probe_mats =  dir([probe_feat_dir,'*.mat']);
probe_feat_all = [];
for i=1:size(probe_mats, 1)
    probe_feat_i = importdata([probe_feat_dir, probe_mats(i).name]);
    probe_feat_all = [probe_feat_all;probe_feat_i];
end
probe_feat_all = normalize_feat(probe_feat_all, 4);
probe_feat_index = probe_feat_all(:, 1:3);
probe_feat_t = probe_feat_all(: ,4:end);
probe_index = unique(probe_feat_index(:, 1));
score_all_action = [];
for video_id = 1:243
    feat = importdata([gallery_feat_dir,'\',num2str(video_id), '.mat']);
    feat = normalize_feat(feat, 4);
    
    gallery_feat_index = feat(:, 1:3);
    gallery_feat_t = feat(:, 4:end);
    
    shots = unique(gallery_feat_index(:, 2));
    
    score_cur = zeros(length(shots), length(probe_index));
    
    score_mat = gallery_feat_t*probe_feat_t';
    
    for probe_i = 1:length(probe_index)
        cur_p_index = probe_index(probe_i);
        index_p = (probe_feat_index(:, 1)==cur_p_index);
        
        for shot_i =1:length(shots)
            cur_shot_index = shots(shot_i);
            index_s = (gallery_feat_index(:, 2)==cur_shot_index);
            score_cur(cur_shot_index, cur_p_index) = max(max(score_mat(index_s, index_p)));
        end
    end
    clear score_mat
    
    score_cur  = [ones(length(shots), 1)*video_id, shots, score_cur];
    score_all_action = cat(1, score_all_action, score_cur);
  %  save(['scores\', num2str(video_id)], 'score_cur');
    fprintf('the video %d has done\n', video_id);
end
save('scores/action_shot_score_all','score_all_action');