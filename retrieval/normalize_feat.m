function out = normalize_feat(feat, begin_index)
out_index = feat(:, 1:begin_index-1);
feat_t = feat(:, begin_index:end);

mean_f = mean(feat_t, 1);
feat_t = bsxfun(@minus, feat_t, mean_f);

feat_norm = sqrt(sum(feat_t.*feat_t, 2));

out_value = bsxfun(@rdivide, feat_t, feat_norm);
out = [out_index, out_value];
disp('normalized feature!');