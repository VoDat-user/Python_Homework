import pandas as pd
 
# # Create DataFrame
# df_input = pd.DataFrame(
#     [['apple', 'banana', 'cherry'], 
#      ['date', None, 'fig']]
# )

# df = pd.DataFrame(
#     [['ant', 'bee', 'cat'], 
#      ['dog', None, 'fly']]
# )

# # Display original DataFrames
# print("\nOriginal df_input:")
# print(df_input)
# print("\nOriginal df:")
# print(df)

# # Check for null values
# print("\nNull values in df:")
# print(pd.isnull(df))

# # Drop NA values
# df_dropped = df.dropna()
# print("\nAfter dropping NA values:")
# print(df_dropped)

# # Fill NA values
# df_filled = df_input.fillna(value="missing")
# print("\nAfter filling NA values:")
# print(df_filled)

#merge DataFrames
df1 = pd.DataFrame({
    'A': ['foo', 'bar', 'baz'],
    'B': [1, 2, 3]
})
# print(df1)

df2 = pd.DataFrame({
    'A': ['foo', 'bar', 'qux'],
    'C': [4, 5, 6]
})
# print(df2)

# Merge hai DataFrame dựa trên cột 'A'
df_merged = df1.merge(df2, on='A')
print("\nMerged DataFrame:")
print(df_merged)
