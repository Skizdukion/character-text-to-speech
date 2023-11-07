rm -rf bark
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/suno/bark
cd bark
echo "Pull text_2.pt"
git lfs pull --include "text_2.pt"
echo "Pull coarse_2.pt"
git lfs pull --include "coarse_2.pt"
echo "Pull fine_2.pt"
git lfs pull --include "fine_2.pt"