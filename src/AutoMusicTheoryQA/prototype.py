from dataclasses import dataclass
import re
import music21
from fractions import Fraction

@dataclass
class MusicTheorySingleChoiceQuestion:
    question:str
    abc_context:str
    correct_answer: str
    incorrect_answer1:str 
    incorrect_answer2:str 
    incorrect_answer3:str
    catagory:str
    difficulty:str
    
class MusicSheet:
   
    def __init__(self, abc_string: str) -> None:
        """
        初始化 MusicSheet 对象。

        Args:
            abc_string (str): 包含完整 abc 乐谱的字符串。
        """
        self._abc_string = abc_string
        try:
            # music21 的核心功能：解析字符串为乐谱对象
            self.score = music21.converter.parse(abc_string, format='abc')
        except Exception as e:
            # 如果解析失败，则 score 为 None
            print(f"Warning: music21 failed to parse ABC string. Error: {e}")
            self.score = None
        self._header_lines = []
        self._body_lines = []
        # 解析并分离谱头和谱身
        self._parse()
        

    def _parse(self) -> None:
      
        lines = self._abc_string.strip().split('\n')
        
        # 正则表达式，用于匹配谱头行，例如 "T:Cooley's"
        header_pattern = re.compile(r"^[A-Z]:")
        
        header_ended = False
        for line in lines:
            if not line.strip() or line.strip().startswith('%'):
                continue
            if header_ended:
                self._body_lines.append(line)
            elif header_pattern.match(line):
                self._header_lines.append(line)
            else:
                header_ended = True
                self._body_lines.append(line)
    
    @property
    def key(self) -> music21.key.Key:
        """使用 music21 的分析功能获取调性对象。"""
        if self.score:
            # .analyze('key') 是一个非常强大的调性分析功能
            return self.score.analyze('key')
        return None

    @property
    def time_signature(self):
        """从乐谱流中获取拍号对象。"""
        if self.score:
            # 从乐谱流中直接获取拍号信息
            ts = self.score.getTimeSignatures()
            if ts:
                return ts[0]
        return None
    
    @property
    def default_note_length(self) -> Fraction:
        """从乐谱流中获取拍号对象。"""
        header=self.header
        numerator,denominator=re.findall(r"L:\s*(\d+)/(\d+)",header)[0]
        return Fraction(int(numerator), int(denominator))
    @property
    def header(self) -> str:
        """
        返回乐谱的谱头部分。

        Returns:
            str: 包含所有谱头信息的字符串，各行由换行符分隔。
        """
        return "\n".join(self._header_lines)
    
    @property
    def body(self) -> str:
        """
        返回乐谱的谱身部分。

        Returns:
            str: 包含所有音符和音乐指令的字符串，各行由换行符分隔。
        """
        return "\n".join(self._body_lines)
    

    def get_first_n_measure(self, n: int, skip_first=True,drop_chord=False) -> str:
        """
        从谱身中提取前 n 个小节。

        这个方法会处理跨行的小节，并将它们连接起来返回。
        
        Args:
            n (int): 需要提取的小节数量。

        Returns:
            str: 一个包含前 n 个小节的字符串，小节之间用 '|' 分隔。
        """
        if n <= 0:
            return ""
            
        body_content = []
        for line in self._body_lines:
            line_without_comment = line.split('%')[0].strip()
            if line_without_comment:
                body_content.append(line_without_comment)

        full_body_str = "".join(body_content)

        measures = full_body_str.split('|')
        
        valid_measures = [measure.strip() for measure in measures if measure.strip()]
        if skip_first==True:
            first_n_measures = valid_measures[1:n+1]
        else:
            first_n_measures = valid_measures[0:n]
        
        if not first_n_measures:
            return ""
        ret="|" + "|".join(first_n_measures) + "|"
        ret = re.sub(r'(:\|)|(\|:)', '|', ret)
        ret = re.sub(r'\|', ' | ', ret)
        if drop_chord:
            ret=re.sub(r'".*?"',"",ret)
        ret = re.sub(r'\s+'," ",ret).strip()
        return ret
    
class BasePrototype:
    @staticmethod
    def produce(self,music_sheet:MusicSheet)-> MusicTheorySingleChoiceQuestion:
        raise NotImplementedError()
    
