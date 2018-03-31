function toThousands(num){
  var str_num = String(num).split('.');
  if (str_num.length == 1) {      // 无小数点
    return (num || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,') + '.00';
  }else if (str_num[1].length == 1) {
    return (str_num[0] || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,') + '.' + str_num[1] + '0';
  }else if (str_num[1].length == 2) {
    return (str_num[0] || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,') + '.' + str_num[1];
  }else if (str_num[1].length > 2) {
    return (str_num[0] || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,') + '.' + str_num[1].slice(0, 2);
  }
}

function toPercents(num){
  if (num === null) {
    return '';
  }else{
    return (num*100).toFixed(2) + '\%';
  }
}

// 浮点精确四则运算
function accAdd(arg1, arg2) {
  var re = new RegExp(",", "g");
  arg1 = arg1.toString().replace(re, '');
  arg2 = arg2.toString().replace(re, '');
  var r1, r2, m;
  try {r1 = arg1.toString().split(".")[1].length} catch(e) {r1 = 0};
  try {r2 = arg2.toString().split(".")[1].length} catch(e) {r2 = 0};
  m = Math.pow(10, Math.max(r1, r2));
  return (arg1 * m + arg2 * m) / m;
}
function accMinus(arg1, arg2) {
  var re = new RegExp(",", "g");
  arg1 = arg1.toString().replace(re, '');
  arg2 = arg2.toString().replace(re, '');
  return accAdd(arg1, -arg2)
}
function accMul(arg1, arg2) {
  var re = new RegExp(",", "g");
  arg1 = arg1.toString().replace(re, '');
  arg2 = arg2.toString().replace(re, '');
  var m = 0, s1 = arg1.toString(), s2 = arg2.toString();
  try {m += s1.split(".")[1].length} catch(e) {};
  try {m += s2.split(".")[1].length} catch(e) {};
  return Number(s1.replace(".", "")) * Number(s2.replace(".", "")) / Math.pow(10, m);
}
function accDiv (arg1, arg2) {
  var re = new RegExp(",", "g");
  arg1 = arg1.toString().replace(re, '');
  arg2 = arg2.toString().replace(re, '');
  var t1 = 0, t2 = 0, r1, r2;
  try {t1 = arg1.toString().split(".")[1].length} catch(e) {};
  try {t2 = arg2.toString().split(".")[1].length} catch(e) {};
  with (Math) {
      r1 = Number(arg1.toString().replace(".", ""));
      r2 = Number(arg2.toString().replace(".", ""));
      return (r1 / r2) * pow(10, t2 - t1);
  }
}

function makeChart(div_id, chart_data, chart_title, item_describe) {
  var myChart = echarts.init(document.getElementById(div_id));
  option = {
      title : {
          text: chart_title,
          left: 'center',
      },
      tooltip : {
          trigger: 'item',
          formatter: "{b} <br/>{a} : {c} ({d}%)"
      },
      series : [
          {
              name: item_describe,
              type: 'pie',
              radius: '55%',
              center: ['50%', '60%'],
              label: {
                normal: {show: true, },
              },
              data: chart_data,
          }
      ],
  };
  myChart.setOption(option);
}

function twoListToOneDict (list1, list2) {
  var dictionary = {};
  var index;
  for (index in list1) {
    dictionary[list1[index]] = list2[index];
  }
  return dictionary;
}

function Stack(){
    this.data = [];
    this.push = push;        //添一个或多个元素到栈顶
    this.pop = pop;          //移除栈顶的元素，同时返回被移除的元素
    this.peek = peek;        //返回栈顶的元素
    this.isEmpty = isEmpty;  //判断栈是否为空，空返回true，否则返回false
    this.clear = clear;      //移除栈里的所有元素
    this.size = size;        //返回栈内元素的个数
  function push(ele){
      this.data.push(ele);
  };
  function pop(){
      return this.data.pop();  //利用数组的pop()方法来达到移除栈顶的元素，同时返回被移除的元素
  };
  function peek(){
      return this.data[this.data.length-1]
  };
  function isEmpty(){
      return this.data.length == 0;
  };
  function size(){
      return this.data.length;
  };
  function clear(){
      this.data = [];
  };
};

// 定义一个队列
function Queue(){
        this.dataStore = [];
        this.enqueue = enqueue;
        this.dequeue = dequeue;
        this.front = front;
        this.back = back;
        this.toString = toString;
        this.isEmpty = isEmpty;
  //入队，就是在数组的末尾添加一个元素
  function enqueue(element){
      this.dataStore.push(element);
  }
  //出队，就是删除数组的第一个元素
  function dequeue(){
      return this.dataStore.shift();
  }
  //取出数组的第一个元素
  function front(){
      return this.dataStore[0];
  }
  //取出数组的最后一个元素
  function back(){
      return this.dataStore[this.dataStore.length-1];
  }

  function toString(){
      var retStr = "";
      for (var i=0; i<this.dataStore.length; ++i) {
          retStr += this.dataStore[i] + "&nbsp;"
      }
      return retStr;
  }
  //判断数组是否为空
  function isEmpty(){
      if(this.dataStore.length == 0){
          return true;
      }else{
          return false;
      }
  }
  //返回数组中元素的个数
  function count(){
      return this.dataStore.length;
  }
};

String.prototype.trim = function() {
  return this.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
};

function caluByRpn(expression, printLog=false) {
  // 可以计算运算符宽度为1的四则运算，缺少检查合法性环节，明天将运算符扩展为多位
  // expression += '\0';
  // 运算符优先级表
  var dict_priority = {
    '!':       10,
    '^':       9,
    '/':       8,
    '*':       8,
    '-':       7,
    '+':       7,
    '=>':      6, // 包含
    '!>':      6, // 不包含
    '>':       6,
    '<':       6,
    '>=':      6,
    '<=':      6,
    '=':       5,
    '!=':      5,
    '&&':      4,
    '||':      3,
    '(':       2,
    ')':       1,
    '\0':     -1,
  };
  var queueExpression = new Queue();              // 建立预处理队列queueExpression用于后续运算
  var queueOperand = new Queue(); var A;          // 建立运算数队列queueOperand用于运算数的存储
  var stackOperator = new Stack(); var B;         // 建立运算符栈stackOperator用于运算符的存储
  stackOperator.push('\0');
  // 创建预处理队列：queueExpression
  var pattern = '';                               // 构造算符字符检测正则表达式
  var pattern_multi = '';                         // 构造多位算符字符检测正则表达式
  var pattern_test = '';                          // 构造算符匹配正则表达式
  var pattern_multi_test = '';                    // 构造多位算符匹配正则表达式
  for (var operator in dict_priority) {
    if (operator == '\0') {break};
    pattern += (pattern.indexOf('\\'+operator[0]) >= 0) ? '' : ((pattern.length > 0) ? '|\\' : '\\')+operator[0];
    pattern_test += ((pattern_test.length > 0) ? '|\\' : '\\')+operator[0] + ((operator.length == 2) ? '\\'+operator[1] : '');
    if (operator.length == 2) {
      pattern_multi += (pattern_multi.indexOf('\\'+operator[0]) >= 0) ? '' : ((pattern_multi.length > 0) ? '|\\' : '\\')+operator[0];
      pattern_multi_test += ((pattern_multi_test.length > 0) ? '|\\' : '\\')+operator[0] + ((operator.length == 2) ? '\\'+operator[1] : '');
    };
  };
  var pattern = RegExp(pattern);
  var pattern_multi = RegExp(pattern_multi);
  var pattern_test = RegExp(pattern_test);
  var pattern_multi_test = RegExp(pattern_multi_test);
  var i;
  var A;
  while (expression.search(pattern) >= 0) {
    i = expression.search(pattern);              // 找出运算符的位置
    A = expression.substring(0, i).trim();       // 将运算符之前的数提取出来，去掉两边的空格后压入预处理队列
    if (A.length > 0) {
      queueExpression.enqueue(A);
    }
    if (pattern_multi.test(expression[i]) && pattern_multi_test.test(expression.substring(i, i+2))) {    // 如果该算符有有2位的可能性，就检测这2位是否是一个算符
      queueExpression.enqueue(expression.substring(i, i+2));     // 将该2位运算符压入预处理队列
      if (printLog) {console.log('检测到算符：', expression.substring(i, i+2))};
      i++;
    }else{
      queueExpression.enqueue(expression[i]);     // 将该1位运算符压入预处理队列
      if (printLog) {console.log('检测到算符：', expression[i])};
    };
    expression = expression.substring(i+1);     // 将expression截短
  };
  if (expression.length > 0) {
    queueExpression.enqueue(expression.trim());
  };
  // 正负号前补0
  for (i in queueExpression.dataStore) {
    if (queueExpression.dataStore[i] == '+' || queueExpression.dataStore[i] == '-') {
      if (i == 0) {
        queueExpression.dataStore.splice(0, 0, '0');
      }else if (queueExpression.dataStore[i-1] == '(') {
        queueExpression.dataStore.splice(i, 0, '0');
      };
    };
  };
  if (printLog) {console.log('预处理队列：', queueExpression.dataStore)};
  // 遍历预处理队列
  while (!queueExpression.isEmpty()) {
    A = queueExpression.dequeue();
    // 如果A是个运算数，就压入运算数栈
    if (!pattern_test.test(A)) {
      queueOperand.enqueue(A);
      if (printLog) {console.log(`将【${A}】压入队列`)};
    }
    // 如果A是左括号，就压入运算符栈
    else if (A == '(') {
      stackOperator.push(A);
      if (printLog) {console.log(`将【${A}】压入符栈`)};
    }
    // 如果A是右括号
    else if (A == ')') {
      // 如果运算符栈顶不是左括号，就将运算符栈顶的元素弹出，并压入运算数队列
      while (stackOperator.peek() != '(') {
        B = stackOperator.pop();
        queueOperand.enqueue(B);
        if (printLog) {console.log(`将符栈顶元素【${B}】压入队列`)};
      };
      // 如果运算符栈顶是左括号，就将运算符栈顶的元素弹出
      if (stackOperator.peek() == '(') {
        B = stackOperator.pop();
        if (printLog) {console.log(`将【${B}】踢出符栈`)};
      };
    }
    // 如果A是运算符
    else if (pattern_test.test(A)) {
      // 当A的优先级<=运算符栈顶元素的优先级，就将运算符栈顶的元素弹出，并压入运算数队列
      while (dict_priority[A] <= dict_priority[stackOperator.peek()]) {
        B = stackOperator.pop();
        queueOperand.enqueue(B);
        if (printLog) {console.log(`将符栈顶元素【${B}】压入队列`)};
      };
      // 当A的优先级>运算符栈顶元素的优先级，就将运算符栈顶的元素弹出
      if (dict_priority[A] > dict_priority[stackOperator.peek()]) {
        stackOperator.push(A);
        if (printLog) {console.log(`将【${A}】压入符栈`)};
      };
    };
  };

  // 扫描完成后，把Operator栈的元素依次出栈，然后依次压入Operand队列中。
  while (stackOperator.peek() != '\0') {
    B = stackOperator.pop();
    queueOperand.enqueue(B);
    if (printLog) {console.log(`将符栈顶元素【${B}】压入队列`)};
  };

  if (printLog) {console.log('逆波兰表达式为：', queueOperand.dataStore)};

  // 构造一个运算结果中间变量，一个运算结果栈
  var result, fisrt_arg, second_arg;
  var stackResult = new Stack();
  while (!queueOperand.isEmpty()) {
    var A = queueOperand.dequeue();
    if (!pattern_test.test(A)) {
      stackResult.push(A);
      if (printLog) {console.log(`将【${A}】压入结果栈`)};
    }else if (dict_priority[A] > 0) {
      if (A == '+') {     // 如果为二元算符
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = accAdd(fisrt_arg, second_arg);
        if (printLog) {console.log(`计算【${fisrt_arg}】+【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '-') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = accMinus(fisrt_arg, second_arg);
        if (printLog) {console.log(`计算【${fisrt_arg}】-【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '*') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = accMul(fisrt_arg, second_arg);
        if (printLog) {console.log(`计算【${fisrt_arg}】*【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '/') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = accDiv(fisrt_arg, second_arg);
        if (printLog) {console.log(`计算【${fisrt_arg}】/【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '^') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = Math.pow(fisrt_arg, second_arg);
        if (printLog) {console.log(`计算【${fisrt_arg}】^【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '>') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = fisrt_arg > second_arg;
        if (printLog) {console.log(`计算【${fisrt_arg}】>【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '<') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = fisrt_arg < second_arg;
        if (printLog) {console.log(`计算【${fisrt_arg}】<【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '=') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = fisrt_arg == second_arg;
        if (printLog) {console.log(`计算【${fisrt_arg}】==【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '>=') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = fisrt_arg >= second_arg;
        if (printLog) {console.log(`计算【${fisrt_arg}】>=【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '<=') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = fisrt_arg <= second_arg;
        if (printLog) {console.log(`计算【${fisrt_arg}】<=【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '!=') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = fisrt_arg != second_arg;
        if (printLog) {console.log(`计算【${fisrt_arg}】!=【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '&&') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = fisrt_arg && second_arg;
        if (printLog) {console.log(`计算【${fisrt_arg}】AND【${second_arg}】=【${result}】压入结果栈`)};
      }else if (A == '||') {
        second_arg = stackResult.pop();
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】、【${second_arg}】弹出结果栈`)};
        result = fisrt_arg || second_arg;
        if (printLog) {console.log(`计算【${fisrt_arg}】OR【${second_arg}】=【${result}】压入结果栈`)};
      }
      //以下为一元算符
      else if (A == '!') {
        fisrt_arg = stackResult.pop();
        if (printLog) {console.log(`将【${fisrt_arg}】弹出结果栈`)};
        result = !fisrt_arg;
        if (printLog) {console.log(`计算NOT 【${fisrt_arg}】=【${result}】压入结果栈`)};
      }

      stackResult.push(result);
    }
  };

  return stackResult.peek();
};

function compareObject(x, y) {
  // If both x and y are null or undefined and exactly the same
  if (x === y) {
    return true;
  }
  // If they are not strictly equal, they both need to be Objects
  if (!(x instanceof Object) || !(y instanceof Object)) {
    return false;
  }
  //They must have the exact same prototype chain,the closest we can do is
  //test the constructor.
  if (x.constructor !== y.constructor) {
    return false;
  }
  for (var p in x) {
    //Inherited properties were tested using x.constructor === y.constructor
    if (x.hasOwnProperty(p)) {
      // Allows comparing x[ p ] and y[ p ] when set to undefined
      if (!y.hasOwnProperty(p)) {
        return false;
      }
      // If they have the same strict value or identity then they are equal
      if (x[p] === y[p]) {
        continue;
      }
      // Numbers, Strings, Functions, Booleans must be strictly equal
      if (typeof(x[p]) !== "object") {
        return false;
      }
      // Objects and Arrays must be tested recursively
      if (!Object.equals(x[p], y[p])) {
        return false;
      }
    }
  }
  for (p in y) {
    // allows x[ p ] to be set to undefined
    if (y.hasOwnProperty(p) && !x.hasOwnProperty(p)) {
      return false;
    }
  }
  return true;
};


function getDataFromUser(head_type) {
  // 取得各字段数据并格式化之
  var data = {};
  for (var key in head_type) {
    var value = $('#id_' + key).val();
    // console.log(key, value);
    if (value === '') {
      value = null
    }else if (head_type[key] == '整数型') {
      value = parseInt(value.replace(/\,/g, '') || 0);
    }else if (head_type[key] == '浮点型') {
      value = parseFloat(value.replace(/\,/g, '') || 0);
    }else if (head_type[key] == '百分比') {
      value = parseFloat(value.replace(/\%/g, '') || 0) / 100;
    };
    data[key] = value;
  };
  // 返回数据
  return data;
};
function DictIsEqual(dict1, dict2) {
  for (var key in dict1) {
    if (dict1[key] !== dict2[key]) {
      // console.log(key, dict1[key], dict2[key]);
      return false;
    };
  };
  return true;
};