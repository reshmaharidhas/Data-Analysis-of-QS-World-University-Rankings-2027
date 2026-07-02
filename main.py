import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import plotly.express as px
import streamlit as st

@st.cache_data
# Function to load the dataset in CSV format into dataframe.
def load_data():
    qs_world_ranking_2027 = pd.read_csv("data/cleaned_qs_world_rankings_2027.csv")
    qs_world_ranking_2027.drop(columns=["Unnamed: 0"], inplace=True)
    return qs_world_ranking_2027

# Setting page configurations
st.set_page_config(layout="wide",page_title="QS 2027 Dashboard",page_icon="🎓")
# Calling the function to load dataset.
qs_world_ranking_2027 = load_data()
# Header of the dashboard.
st.header("🎓QS World University ranking 2027 Dashboard🌏")
# Sidebar widget to choose region
region_selected = st.sidebar.selectbox("Region",options=qs_world_ranking_2027["region"].unique())
# Sidebar widget to choose specific country under selected region.
country_selected = st.sidebar.selectbox('Country',options=qs_world_ranking_2027[qs_world_ranking_2027["region"]==region_selected]["country/territory"].unique())
# Sidebar widget to choose specific university under the selected country.
university_selected = st.sidebar.selectbox('University',options=qs_world_ranking_2027[qs_world_ranking_2027["country/territory"]==country_selected]["institution_name"])
# Mapping terms
factors_col_name_dict = {"AR score":"ar_score","ER score":"er_score","QS 2027 Rank":"2027_rank_numeric","FSR score":"fsr_score","CPF score":"cpf_score","IFR score":"ifr_score","ISR score":"isr_score","IRN score":"irn_score","EO score":"eo_score","SUS score":"sus_score"}
size_university_mapping = {"S":"Small","M":"Medium","L":"Large","XL":"Extra Large"}
research_university_mapping = {"VH":"Very High","HI":"High","MD":"Medium","LO":"Low"}
focus_university_mapping = {"FC":"Full Comprehensive","CO":"Comprehensive","FO":"Focused","SP":"Specialist"}

# Tabs
home_tab, country_wise_tab, university_tab,compare_tab= st.tabs(["🌏Region-wise","🌐Country-wise","🏫University","📊Compare universities"])
# Home tab (Region tab)
with home_tab:
    # Row of KPI metrics.
    with st.container(horizontal=True):
        with st.container(border=True,gap=None):
            st.metric(label="Total Universities",value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['region']==region_selected].shape[0]}**")
        with st.container(border=True,gap=None):
            st.metric(label="Total Countries",value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['region']==region_selected]['country/territory'].value_counts().shape[0]}**")
        with st.container(border=True,gap=None):
            st.metric(label="🏆Top rank",value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['region']==region_selected].head(1)['2027_rank'].unique()[0]}**")
        with st.container(border=True,gap=None):
            st.metric(label="Max overall score",value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['region']==region_selected].head(1)['overall_score'].unique()[0]}**")
        with st.container(border=True,width="content",gap=None):
            st.metric(label='Average Academic Reputation',value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['region']==region_selected]['ar_score'].mean().round(2)}**")
    # Container with sunburst chart and top 10 universities under the selected region.
    with st.container(border=True,horizontal=True):
        with st.container(gap=None):
            cities_grouped_by_avg_overall_score = qs_world_ranking_2027[qs_world_ranking_2027['region']==region_selected].groupby("city")["overall_score"].mean().sort_values(ascending=False)
            fig = px.sunburst(qs_world_ranking_2027[qs_world_ranking_2027["region"]==region_selected],path=["region","country/territory","city"],values="overall_score",title=f"Countries & Cities in {region_selected} by Overall score")
            st.plotly_chart(fig)
        with st.container():
            st.markdown(f"##### 🏫 Top 10 universities in {region_selected} region")
            df = qs_world_ranking_2027[qs_world_ranking_2027['region']==region_selected].head(10)
            with st.container():
                for row in df.itertuples(index=True):
                    st.write(f"📗 {row.institution_name}")
    # Fragment
    @st.fragment
    # Function to display distribution of various scores of countries in the selected region as box plot.
    def display_distribution_of_region_wise_scores():
        with st.container(border=True,gap=None):
            pill_selected = st.pills("Scores",options=["QS 2027 Rank","AR score","ER score","FSR score","CPF score","IFR score","ISR score","IRN score","EO score","SUS score"],selection_mode="single",default="AR score",label_visibility="hidden")
            fig = px.box(qs_world_ranking_2027[qs_world_ranking_2027["region"]==region_selected],x="country/territory",
                         y=factors_col_name_dict.get(pill_selected),color_discrete_sequence=["green"],
                         labels={"country/territory":"Country",factors_col_name_dict.get(pill_selected):pill_selected},
                         title=f"Distribution of {pill_selected} in countries of {region_selected} region")
            fig.update_layout(title_font_color="black",xaxis_title_font_color="black",yaxis_title_font_color="black",
                              xaxis=dict(tickfont=dict(color="black")),yaxis=dict(tickfont=dict(color="black")),
                              hoverlabel=dict(font_color="black"))
            st.plotly_chart(fig)
    # Calling the function to display the distribution of various scores in selected region as box plot.
    display_distribution_of_region_wise_scores()

# Country tab
with country_wise_tab:
    with st.container(horizontal=True):
        with st.container(border=True):
            st.metric(label="Total universities",value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected].shape[0]}**")
        with st.container(border=True):
            st.metric(label="Total cities",value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['city'].value_counts().shape[0]}**")
        with st.container(border=True):
            st.metric(label="🏆Top rank",value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['2027_rank'].unique()[0]}**")
        with st.container(border=True,width="content"):
            st.metric(label='Average AR score',value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['ar_score'].mean().round(2)}**")
        with st.container(border=True,width="content"):
            st.metric(label='Average ER score',value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['er_score'].mean().round(2)}**")
        with st.container(border=True,width="content"):
            st.metric(label='Average FSR score',value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['fsr_score'].mean().round(2)}**")
    with st.container(horizontal=True):
        with st.container(border=True):
            st.metric(label='Average CPF score',value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['cpf_score'].mean().round(2)}**")
        with st.container(border=True,width="content"):
            if pd.isna(qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['ifr_score'].mean())==True:
                st.metric(label='Average IFR score',value=0)
            else:
                st.metric(label='Average IFR score',value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['ifr_score'].mean().round(2)}**")
        with st.container(border=True,width="content"):
            if pd.isna(qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['isr_score'].mean())==True:
                st.metric(label="Average ISR score",value=0)
            else:
                st.metric(label='Average ISR score',value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected]['isr_score'].mean().round(2)}**")
        with st.container(border=True, width="content"):
            st.metric(label='Average IRN score',
                      value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory'] == country_selected]['irn_score'].mean().round(2)}**")
        with st.container(border=True, width="content"):
            st.metric(label='Average EO score',
                      value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory'] == country_selected]['eo_score'].mean().round(2)}**")
        with st.container(border=True, width="content"):
            if pd.isna(qs_world_ranking_2027[qs_world_ranking_2027['country/territory'] == country_selected]['sus_score'].mean())==True:
                st.metric(label="Average SUS score",value=0)
            else:
                st.metric(label='Average SUS score',
                      value=f"**{qs_world_ranking_2027[qs_world_ranking_2027['country/territory'] == country_selected]['sus_score'].mean().round(2)}**")
    with st.container():
        country_section_1, country_section_2 = st.columns(2)
        # Displaying pie chart of cities in country selected with overall score.
        with country_section_1:
            with st.container():
                #fig = px.pie(qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected],names="city",values="overall_score")
                fig = px.sunburst(qs_world_ranking_2027[qs_world_ranking_2027["country/territory"]==country_selected],path=["country/territory","city"],values="overall_score",title=f"Cities in {country_selected} by overall score")
                fig.update_layout(title_font_color="black", xaxis_title_font_color="black",
                                  yaxis_title_font_color="black",
                                  xaxis=dict(tickfont=dict(color="black")), yaxis=dict(tickfont=dict(color="black")),
                                  hoverlabel=dict(font_color="black"))
                st.plotly_chart(fig,key="country_city_sunburst_chart")
        # Displaying list of colleges in selected country by rank.
        with country_section_2:
            @st.fragment
            def display_universities_in_country_by_factor():
                with st.container(border=True,height=430,gap="xsmall"):
                    st.markdown(f"###### Ranking universities in {country_selected}")
                    country_factor_selected = st.selectbox("Sort by",options=["QS 2027 Rank","AR score","ER score","FSR score","CPF score","IFR score","ISR score","IRN score","EO score","SUS score"])
                    if country_factor_selected=="QS 2027 Rank":
                        df = qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected].sort_values(by=[factors_col_name_dict.get(country_factor_selected)])
                    else:
                        df = qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected].sort_values(by=[factors_col_name_dict.get(country_factor_selected)],ascending=False)
                    st.table(df[["institution_name",factors_col_name_dict.get(country_factor_selected)]],hide_index=True,border="horizontal")
            # Calling the fragment function in country-wise tab.
            display_universities_in_country_by_factor()
    # Container to display various scores as ECDF chart.
    with st.container():
        with st.container(border=True):
            st.markdown(f"##### Distribution of scores in {country_selected}")
            fig = px.ecdf(qs_world_ranking_2027[qs_world_ranking_2027['country/territory'] == country_selected],
                          x=["ar_score", "er_score", "fsr_score", "cpf_score", "ifr_score", "isr_score", "irn_score",
                             "eo_score"], ecdfnorm=None,height=350,markers=True)
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            fig.update_layout(title_font_color="black", xaxis_title_font_color="black", yaxis_title_font_color="black",
                              xaxis=dict(tickfont=dict(color="black")), yaxis=dict(tickfont=dict(color="black")),hoverlabel=dict(font_color="black"))
            st.plotly_chart(fig, key="country_ar_score_hist_chart")
    with st.container():
        country_section_3, country_section_4 = st.columns(2)
        with country_section_3:
            with st.container(border=True):
                fig = px.bar(qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected],y="research",x="overall_score",height=200,labels={'overall_score':"Overall score","research":"Research"})
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                fig.update_layout(title_font_color="black",xaxis_title_font_color="black",yaxis_title_font_color="black",
                                  xaxis=dict(tickfont=dict(color="black")),yaxis=dict(tickfont=dict(color="black")),hoverlabel=dict(font_color="black"))
                st.plotly_chart(fig,key="country_research_chart")
            with st.container(border=True):
                fig = px.bar(qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected],y="status",x="overall_score",height=200,labels={'overall_score':"Overall score","status":"Institution type"})
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                fig.update_layout(title_font_color="black", xaxis_title_font_color="black",
                                  yaxis_title_font_color="black",
                                  xaxis=dict(tickfont=dict(color="black")), yaxis=dict(tickfont=dict(color="black")),
                                  hoverlabel=dict(font_color="black"))
                st.plotly_chart(fig,key="country_institution_type_chart")
        with country_section_4:
            with st.container(border=True):
                fig = px.bar(qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected],y="size",x="overall_score",height=200,labels={'overall_score':"Overall score","size":"Size"})
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                fig.update_layout(title_font_color="black", xaxis_title_font_color="black",yaxis_title_font_color="black",
                                  xaxis=dict(tickfont=dict(color="black")), yaxis=dict(tickfont=dict(color="black")),
                                  hoverlabel=dict(font_color="black"))
                st.plotly_chart(fig,key="country_size_chart")
            with st.container(border=True):
                f, ax = plt.subplots(figsize=(7,3))
                seaborn.countplot(qs_world_ranking_2027[qs_world_ranking_2027['country/territory']==country_selected],y="2027_rank_status",ax=ax,width=0.35,color="blue")
                ax.set_ylabel("Rank change status")
                ax.set_xlabel("Count of universities")
                st.write(f)

# University tab
with university_tab:
    with st.container():
        st.markdown(f"#### {university_selected}")
        university_df = qs_world_ranking_2027[qs_world_ranking_2027["institution_name"]==university_selected]
        with st.container(horizontal=True):
            with st.container(border=True,width="content",height=120,gap=None):
                if pd.isna(qs_world_ranking_2027[qs_world_ranking_2027["institution_name"]==university_selected]["rank_difference"].unique()):
                    st.metric(label="🏆QS 2027 rank",value=f"{qs_world_ranking_2027[qs_world_ranking_2027['institution_name']==university_selected]['2027_rank'].unique()[0]}")
                else:
                    latest_rank = qs_world_ranking_2027[qs_world_ranking_2027["institution_name"]==university_selected]["2027_rank_numeric"].unique()[0]
                    previous_rank = qs_world_ranking_2027[qs_world_ranking_2027["institution_name"]==university_selected]["previous_year_rank_numeric"].unique()[0]
                    delta_rank = int(previous_rank-latest_rank)
                    st.metric(label="🏆QS 2027 rank",value=f"{qs_world_ranking_2027[qs_world_ranking_2027['institution_name']==university_selected]['2027_rank'].unique()[0]}",delta=delta_rank)
            with st.container(border=True,height=120):
                st.metric(label="Academic Reputation score",value=university_df["ar_score"].unique()[0])
            with st.container(border=True,height=120):
                st.metric(label="Employer Reputation score",value=university_df["er_score"].unique()[0])
            with st.container(border=True,height=120):
                st.metric(label="Employer Outcome score",value=university_df["eo_score"].unique()[0])
            with st.container(border=True,height=120):
                st.metric(label="Sustainability score",value=university_df["sus_score"].unique()[0])
        with st.container(horizontal=True):
            with st.container(border=True):
                st.metric(label="Faculty Student Ratio score",value=university_df["fsr_score"].unique()[0])
            with st.container(border=True):
                if pd.isna(university_df["cpf_score"].unique()[0])==True:
                    st.metric(label="Citations per Faculty score", value=0)
                else:
                    st.metric(label="Citations per Faculty score",value=university_df["cpf_score"].unique()[0])
            with st.container(border=True):
                if pd.isna(university_df["ifr_score"].unique()[0])==True:
                    st.metric(label="International Faculty Ratio score", value=0)
                else:
                    st.metric(label="International Faculty Ratio score",value=university_df["ifr_score"].unique()[0])
            with st.container(border=True):
                if pd.isna(university_df["isr_score"].unique()[0])==True:
                    st.metric(label="International Student Ratio score",value=0)
                else:
                    st.metric(label="International Student Ratio score",value=university_df["isr_score"].unique()[0])
            with st.container(border=True):
                if pd.isna(university_df["irn_score"].unique()[0])==True:
                    st.metric(label="International Research Network score",value=0)
                else:
                    st.metric(label="International Research Network score",value=university_df["irn_score"].unique()[0])
            with st.container(border=True,width="content"):
                if pd.isna(university_df["overall_score"].unique()[0])==True:
                    st.metric(label="Overall score",value=0)
                else:
                    st.metric(label="Overall score",value=university_df["overall_score"].unique()[0])
        with st.container(horizontal=True):
            with st.container(border=True):
                st.markdown(f"###### Type: {university_df['status'].unique()[0]}")
            with st.container(border=True):
                st.markdown(f"###### Focus: {focus_university_mapping.get(university_df['focus'].unique()[0])}")
            with st.container(border=True,width="content"):
                st.markdown(f"###### Research: {research_university_mapping.get(university_df['research'].unique()[0])}")
            with st.container(border=True,width="content"):
                st.markdown(f"###### Size: {size_university_mapping.get(university_df['size'].unique()[0])}")
        with st.container(border=True,gap=None):
            scope_dictionary = {"Asia":"asia","Africa":"africa","Oceania":"oceania","Europe":"europe","Americas":"north america"}
            north_american_countries = ["United States of America","Canada","Mexico","Costa Rica","Cuba","Puerto Rico","Guatemala","Dominican Republic","Honduras","Panama"]
            europe_asian_countries = ["Northern Cyprus"]
            asian_europe_countries = ["Georgia"]
            fig = px.choropleth(university_df,locations=university_df["country/territory"],locationmode="country names",color_discrete_sequence=["red"],title="Geographical location")
            if region_selected=="Americas":
                if country_selected in north_american_countries:
                    fig.update_layout(geo=dict(scope="north america"))
                else:
                    fig.update_layout(geo=dict(scope="south america"))
            elif region_selected=="Europe":
                if country_selected in europe_asian_countries:
                    fig.update_layout(geo=dict(scope="asia"))
                else:
                    fig.update_layout(geo=dict(scope="europe"))
            elif region_selected=="Asia":
                if country_selected in asian_europe_countries:
                    fig.update_layout(geo=dict(scope="europe"))
                else:
                    fig.update_layout(geo=dict(scope="asia"))
            else:
                fig.update_layout(geo=dict(scope=scope_dictionary.get(university_df["region"].unique()[0])))
            fig.update_geos(showocean=True,showland=True,landcolor="sandybrown")
            st.plotly_chart(fig)

# Compare universities tab
with compare_tab:
    # Fragment
    @st.fragment
    # Function to compare multiple universities based on multiple scores.
    def compare_universities():
        with st.container():
            # Multiselect widget to choose one or more universities to compare.
            universities_to_compare = st.multiselect("Choose universities",options=qs_world_ranking_2027["institution_name"].sort_values(),key="multiselect_univ_compare")
            df_univ_comparison = qs_world_ranking_2027[qs_world_ranking_2027['2027_rank_numeric']==0]
            # Concatenating all dataframe of chosen multiple universities into one single dataframe.
            for _ in range(len(universities_to_compare)):
                df_univ_comparison = pd.concat([df_univ_comparison,qs_world_ranking_2027[qs_world_ranking_2027["institution_name"]==universities_to_compare[_]]])
            # Multiselect widget to choose one or more factors to compare the chosen universities.
            factors_to_compare = st.multiselect("Choose factors to compare in universities",
                                                options=["AR score", "ER score", "CPF score",
                                                         "FSR score","IFR score","ISR score","IRN score","EO score","SUS score","Overall score"])
            if "AR score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, x="institution_name", y="ar_score",color_discrete_sequence=["#ff0000"],title="Comparison of universities by Academic Reputation score",labels={"institution_name":"University","ar_score":"AR score"},text_auto=True)
                    fig.update_traces(width=0.5)
                    fig.update_layout(title_font_color="black",legend_font_color="black",
                                      xaxis_title_font_color="black",
                                        yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                        yaxis=dict(tickfont=dict(color="black")),
                                      hoverlabel=dict(font_color="black"))
                    st.plotly_chart(fig)
            if "ER score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, x="institution_name", y="er_score",color_discrete_sequence=["orangered"],title="Comparison of universities by Employer Reputation score",labels={"institution_name":"University","er_score":"ER score"},text_auto=True)
                    fig.update_traces(width=0.5)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")),hoverlabel=dict(font_color="black"))
                    st.plotly_chart(fig)
            if "CPF score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, y="institution_name", x="cpf_score",color_discrete_sequence=["gold"],title="Comparison of universities by Citations per Faculty score",labels={"institution_name":"University","cpf_score":"CPF score"},text_auto=True)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")))
                    st.plotly_chart(fig)
            if "FSR score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, y="institution_name", x="fsr_score",color_discrete_sequence=["maroon"],title="Comparison of universities by Faculty Student Ratio score",labels={"institution_name":"University","fsr_score":"FSR score"},text_auto=True)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")))
                    st.plotly_chart(fig)
            if "IFR score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, x="institution_name", y="ifr_score",color_discrete_sequence=["#580aff"],title="Comparison of universities by International Faculty Ratio score",labels={"institution_name":"University","ifr_score":"IFR score"},text_auto=True)
                    fig.update_traces(width=0.5)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")))
                    st.plotly_chart(fig)
            if "ISR score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, x="institution_name", y="isr_score",color_discrete_sequence=["#a1ff0a"],title="Comparison of universities by International Student Ratio score",labels={"institution_name":"University","isr_score":"ISR score"},text_auto=True)
                    fig.update_traces(width=0.5)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")))
                    st.plotly_chart(fig)
            if "IRN score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, x="institution_name", y="irn_score",color_discrete_sequence=["green"],title="Comparison of universities by International Research Network score",labels={"institution_name":"University","irn_score":"IRN score"},text_auto=True)
                    fig.update_traces(width=0.5)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")))
                    st.plotly_chart(fig)
            if "EO score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, x="institution_name", y="eo_score",color_discrete_sequence=["#6f523b"],title="Comparison of universities by Employment Outcome score",labels={"institution_name":"University","eo_score":"EO score"},text_auto=True)
                    fig.update_traces(width=0.5)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")))
                    st.plotly_chart(fig)
            if "SUS score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, x="institution_name", y="sus_score",color_discrete_sequence=["lime"],title="Comparison of universities by Sustainability score",labels={"institution_name":"University","sus_score":"Sustainability score"},text_auto=True)
                    fig.update_traces(width=0.5)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")))
                    st.plotly_chart(fig)
            if "Overall score" in factors_to_compare:
                with st.container(border=True):
                    fig = px.bar(df_univ_comparison, x="institution_name", y="overall_score_numeric",color_discrete_sequence=["#be0aff"],title="Comparison of universities by overall score",labels={"institution_name":"University","overall_score_numeric":"Overall score"},text_auto=True)
                    fig.update_traces(width=0.5)
                    fig.update_layout(title_font_color="black", legend_font_color="black",
                                      xaxis_title_font_color="black",
                                      yaxis_title_font_color="black",
                                      xaxis=dict(tickfont=dict(color="black")),
                                      yaxis=dict(tickfont=dict(color="black")))
                    st.plotly_chart(fig)
    # Calling the fragment function to compare multiple universities based on various factors.
    compare_universities()
