import streamlit as st
import time

st.title('Streamlit 超入門')

st.write('プログレスバーの表示')
'Start!!'

latest_interation = st.empty()
bar = st.progress(0)

for i in range(100):
  latest_interation.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'Done!!'


left_column, right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
  right_column.write('ココは右カラム')

expander = st.expander('問い合わせ')
expander.write('問い合わせ内容を書く')

# text = st.text_input('あなたの趣味を教えてください。')
# condition = st.slider('あなたの今の調子は？', 0, 100, 50)
# 'あなたが趣味:', text
# 'コンディション', condition

# st.sidebar.write('Interactive Widgets')

# text = st.sidebar.text_input('あなたの趣味を教えてください。')
# condition = st.sidebar.slider('あなたの今の調子は？', 0, 100, 50)


# option = st.selectbox(
#   'あなたが好きな数字を教えてください。',
#   list(range(1,11))
# )

# 'あなたが好きな数字は', option, 'です。'

# if st.checkbox('Show Image'):
#   img = Image.open('C_Works.png')
#   st.image(img, caption='test', use_column_width=True)






# df = pd.DataFrame(
#   np.random.rand(100, 2)/[50, 50] + [36.3945194, 139.1034433],
#   columns=['lat', 'lon']
# )

# st.map(df)

# st.table(df.style.highlight_max(axis=0))

# """
# # 章
# ## 節
# ### 項

# ```python
# import streamlit as st
# import numpy as np
# import pandas as pd

# ```

# """

